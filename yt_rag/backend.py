import os
import re

from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

# Lazy imports for heavy ML deps are inside `create_vector_db`.
try:
    from langchain.llms import OpenAI
except Exception:
    try:
        from langchain import OpenAI
    except Exception:
        OpenAI = None

try:
    from langchain_groq import ChatGroq
except Exception:
    ChatGroq = None

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

load_dotenv()


# Initialize an LLM client when keys are available; leave as None otherwise.
if os.environ.get("GROQ_API_KEY") and ChatGroq is not None:
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
else:
    if OpenAI is not None:
        try:
            llm = OpenAI(temperature=0)
        except Exception:
            llm = None
    else:
        llm = None


def _llm_text(response):
    try:
        return response.generations[0][0].text
    except Exception:
        try:
            return response.content
        except Exception:
            return str(response)


def call_llm(prompt: str):
    """Call the configured LLM and return a response-like object.

    This function attempts to call the configured LLM and falls back to a
    friendly message if authentication or configuration is missing.
    """
    def _invoke_current():
        if llm is None:
            raise RuntimeError("No supported call method found on the configured LLM")
        if callable(llm):
            return llm(prompt)
        if hasattr(llm, "invoke"):
            return llm.invoke(prompt)
        if hasattr(llm, "generate"):
            return llm.generate([prompt])
        raise RuntimeError("No supported call method found on the configured LLM")

    try:
        return _invoke_current()
    except Exception as e:
        msg = str(e)
        print("LLM call failed:", msg)

        if ("401" in msg) or ("Invalid API Key" in msg) or ("invalid_api_key" in msg):
            if OpenAI is not None:
                try:
                    print("Falling back to OpenAI due to LLM authentication error.")
                    new_llm = OpenAI(temperature=0)
                    globals()["llm"] = new_llm
                    return call_llm(prompt)
                except Exception as e2:
                    print("OpenAI fallback failed:", e2)

        class _UnavailableResp:
            def __init__(self, content):
                self.content = content

        msg = (
            "LLM unavailable: set OPENAI_API_KEY or GROQ_API_KEY in your environment (.env) to enable LLM features."
        )
        print(msg)
        return _UnavailableResp(msg)


def extract_video_id(url: str) -> str:
    patterns = [r"v=([a-zA-Z0-9_-]{11})", r"youtu\.be/([a-zA-Z0-9_-]{11})"]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("Invalid YouTube URL")


def create_vector_db(url: str):
    video_id = extract_video_id(url)
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    text = " ".join([snippet.text for snippet in transcript])

    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS
    except Exception as e:
        raise ImportError(
            "Missing ML dependencies for vector DB creation. Install 'sentence-transformers', 'langchain-huggingface', and 'langchain-community'"
        ) from e

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_texts(texts=chunks, embedding=embeddings)

    return db, text


def ask_video(db, question: str) -> str:
    docs = db.similarity_search(question, k=8)
    context = "\n".join([doc.page_content for doc in docs])
    if len(question.split()) < 3:
        question = f"Explain {question} in detail with examples."

    prompt = f"""
You are an AI tutor.

Answer using ONLY the lecture context.

Lecture Context:
{context}

Question:
{question}

Provide:
- Clear explanation
- Simple language
- Examples if possible
- Detailed answer

Answer:
"""

    response = call_llm(prompt)
    return _llm_text(response)


def summarize_video(text: str) -> str:
    text = text[:4000]
    prompt = f"""
Create a complete study summary.

Include:

1. Main Topic
2. Important Concepts
3. Key Takeaways
4. Revision Notes
5. Real World Applications

Transcript:

{text}
"""
    response = call_llm(prompt)
    return _llm_text(response)


def generate_interview_questions(text: str) -> str:
    text = text[:4000]
    prompt = f"""
Generate 10 interview questions
with answers.

Transcript:

{text}
"""
    response = call_llm(prompt)
    return _llm_text(response)


def create_pdf(summary: str) -> str:
    pdf_file = "Video_Summary.pdf"
    pdf = SimpleDocTemplate(pdf_file)
    styles = getSampleStyleSheet()
    story = [Paragraph(summary, styles["BodyText"])]
    pdf.build(story)
    return pdf_file
