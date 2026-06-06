
import os
import streamlit as st
from dotenv import load_dotenv

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
