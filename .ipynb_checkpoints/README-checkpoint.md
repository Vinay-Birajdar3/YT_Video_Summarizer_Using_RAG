# YouTube Study Assistant using RAG

## Overview

This project extracts transcripts from YouTube videos and allows users to ask questions about the video content using Retrieval-Augmented Generation (RAG).

## Features

* Extract YouTube transcripts
* Semantic search using FAISS
* Question answering using Gemini
* Video summarization
* MCQ generation
* Interview question generation
* PDF export of summaries

## Technologies Used

* Python
* LangChain
* FAISS
* HuggingFace Embeddings
* Google Gemini
* YouTube Transcript API
* ReportLab

## Project Flow

YouTube URL → Transcript → Chunks → Embeddings → FAISS → Retrieval → Gemini → Answer

## Future Improvements

* Streamlit Web App
* Timestamp-based answers
* Multiple video support
* Chat history
* User authentication
