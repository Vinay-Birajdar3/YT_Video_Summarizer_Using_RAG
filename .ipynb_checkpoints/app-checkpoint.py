
import os
import re
import streamlit as st

from youtube_transcript_api import YouTubeTranscriptApi

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_groq import ChatGroq

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from reportlab.lib.styles import getSampleStyleSheet


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="YouTube Study Assistant",
    page_icon="🎥",
    layout="wide"
)



# ---------------------------------
# GROQ API
# ---------------------------------

os.environ["GROQ_API_KEY"] = "<REDACTED_GROQ_KEY>"

llm = ChatGroq(
    model="llama-3.1-8b-instant"
)


# ---------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------

def extract_video_id(url):

    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})"
    ]

    for pattern in patterns:

        match = re.search(pattern, url)

        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube URL")


def create_vector_db(url):

    video_id = extract_video_id(url)

    ytt_api = YouTubeTranscriptApi()

    transcript = ytt_api.fetch(video_id)

    text = " ".join(
        [snippet.text for snippet in transcript]
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    return db, text


def ask_video(db, question):

    docs = db.similarity_search(
        question,
        k=8
    )

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    if len(question.split()) < 3:
        question = f"Explain {question} in detail with examples."

    prompt = f"""
You are an AI tutor.

Answer the question using the lecture context below.

Instructions:
- Explain clearly.
- Use simple language.
- Give examples if possible.
- Provide a detailed answer.
- If the topic is not present in the lecture, say so.

Lecture Context:
{context}

Question:
{question}

Detailed Answer:
"""

    response = llm.invoke(prompt)

    return response.content


def summarize_video(text):

    text = text[:8000]

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

    response = llm.invoke(prompt)

    return response.content


def generate_interview_questions(text):

    text = text[:8000]

    prompt = f"""
    Generate 10 interview questions
    with answers.

    Transcript:

    {text}
    """

    response = llm.invoke(prompt)

    return response.content


def create_pdf(summary):

    pdf_file = "Video_Summary.pdf"

    pdf = SimpleDocTemplate(
        pdf_file
    )

    styles = getSampleStyleSheet()

    story = [
        Paragraph(
            summary,
            styles["BodyText"]
        )
    ]

    pdf.build(story)

    return pdf_file


# ---------------------------------------------------
# UI
# ---------------------------------------------------

st.title("🎥 YouTube Study Assistant using RAG")

st.markdown(
    """
Paste a YouTube lecture video and automatically generate:

✅ Study Summary

✅ Interview Questions & Answers

✅ PDF Notes

✅ Ask Questions About Video
"""
)

# ---------------------------------------------------
# URL INPUT
# ---------------------------------------------------

url = st.text_input(
    "📺 Paste YouTube URL"
)


# ---------------------------------------------------
# PROCESS VIDEO
# ---------------------------------------------------

if st.button("🚀 Process Video"):

    try:

        with st.spinner("Processing Video..."):

            db, text = create_vector_db(url)

            # Generate summary
            summary = summarize_video(text)

            # Save everything
            st.session_state["db"] = db
            st.session_state["text"] = text
            st.session_state["summary"] = summary

        st.success("✅ Video Processed Successfully!")

    except Exception as e:

        st.error(f"Error: {e}")


# ---------------------------------------------------
# SUMMARY
# ---------------------------------------------------

if "summary" in st.session_state:

    st.divider()

    st.subheader("📝 Video Summary")

    st.write(
        st.session_state["summary"]
    )

    pdf_path = create_pdf(
        st.session_state["summary"]
    )

    with open(
        pdf_path,
        "rb"
    ) as file:

        st.download_button(
            label="📥 Download Summary PDF",
            data=file,
            file_name="Video_Summary.pdf",
            mime="application/pdf"
        )


# ---------------------------------------------------
# GENERATE INTERVIEW QUESTIONS
# ---------------------------------------------------

if "text" in st.session_state:

    st.divider()

    if st.button("🎯 Generate Interview Questions"):

        with st.spinner("Generating Interview Questions..."):

            interview = generate_interview_questions(
                st.session_state["text"]
            )

            st.session_state["interview"] = interview


# ---------------------------------------------------
# INTERVIEW QUESTIONS
# ---------------------------------------------------

if "interview" in st.session_state:

    st.subheader(
        "🎯 Interview Questions & Answers"
    )

    st.write(
        st.session_state["interview"]
    )


# ---------------------------------------------------
# ASK ANYTHING
# ---------------------------------------------------

st.divider()

st.subheader(
    "❓ Ask Anything About This Video"
)

question = st.text_input(
    "Enter your question"
)

if st.button("💬 Ask"):

    if "db" not in st.session_state:

        st.warning(
            "Please process a video first."
        )

    else:

        answer = ask_video(
            st.session_state["db"],
            question
        )

        st.subheader("Answer")

        st.write(answer)