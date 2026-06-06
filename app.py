import streamlit as st
import traceback

st.set_page_config(page_title="YouTube RAG Assistant", layout="centered")
st.title("YouTube RAG Assistant — UI")

try:
    from yt_rag import backend as backend
except Exception:
    try:
        import rag_backend as backend
    except Exception:
        backend = None

if backend is None:
    st.error("Backend not found. Ensure `yt_rag.backend` or `rag_backend` is present.")
    st.stop()

if 'db' not in st.session_state:
    st.session_state['db'] = None

url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
if st.button("Build index"):
    if not url:
        st.warning("Please enter a YouTube URL first.")
    else:
        with st.spinner("Building vector DB (may take a few minutes)..."):
            try:
                res = backend.create_vector_db(url)
                st.session_state['db'] = res
                st.success("Vector DB built and cached in session.")
            except Exception as e:
                st.error(f"Error building vector DB: {e}")
                st.text(traceback.format_exc())

st.write("---")
question = st.text_input("Ask a question about the video")
if st.button("Ask"):
    if st.session_state.get('db') is None:
        st.warning("No vector DB found. Build the index first.")
    elif not question:
        st.warning("Please enter a question.")
    else:
        try:
            answer = backend.ask_video(st.session_state['db'], question)
            st.subheader("Answer")
            st.write(answer)
        except Exception as e:
            st.error(f"Error during QA: {e}")
            st.text(traceback.format_exc())

st.write("---")
if st.button("Generate summary (LLM)"):
    if st.session_state.get('db') is None:
        st.warning("No vector DB found. Build the index first.")
    else:
        try:
            # Some backends expose a summarize function that accepts the DB or text
            if hasattr(backend, 'summarize_video'):
                out = backend.summarize_video(st.session_state['db'])
            else:
                out = "No summarization function available in backend."
            st.subheader("Summary")
            st.write(out)
        except Exception as e:
            st.error(f"Error generating summary: {e}")
            st.text(traceback.format_exc())

st.write("\n\n---\nThis is a minimal UI. For full features use the CLI helpers or see README.")

import os
import streamlit as st
from dotenv import load_dotenv

from yt_rag.backend import (
    create_vector_db,
    summarize_video,
    generate_interview_questions,
    ask_video,
    create_pdf,
)

load_dotenv()

# Warn in the UI if there are no API keys configured
if not (os.environ.get("GROQ_API_KEY") or os.environ.get("OPENAI_API_KEY")):
    st.warning(
        "No LLM API key detected. Set `GROQ_API_KEY` or `OPENAI_API_KEY` in your .env to enable LLM features. "
        "The app will still run but LLM responses will show guidance instead of actual answers."
    )

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="YouTube Study Assistant",
    page_icon="🎥",
    layout="wide"
)

# ---------------------------------------------------
# UI
# ---------------------------------------------------

st.title("🎥 YouTube Study Assistant using RAG")

st.markdown("""
Paste a YouTube lecture and:

✅ Generate Summary

✅ Generate Interview Questions

✅ Ask Questions About Video

✅ Download PDF Notes
""")

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

            summary = summarize_video(text)

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

    with open(pdf_path, "rb") as file:

        st.download_button(
            label="📥 Download Summary PDF",
            data=file.read(),
            file_name="Video_Summary.pdf",
            mime="application/pdf"
        )

# ---------------------------------------------------
# INTERVIEW QUESTIONS
# ---------------------------------------------------

if "text" in st.session_state:

    st.divider()

    if st.button("🎯 Generate Interview Questions"):

        with st.spinner("Generating Interview Questions..."):

            interview = generate_interview_questions(
                st.session_state["text"]
            )

            st.session_state["interview"] = interview

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
            question,
        )

        st.subheader("Answer")

        st.write(answer)
