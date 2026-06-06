# YouTube RAG Assistant
Simple, local YouTube RAG (Retrieval-Augmented Generation)

This project extracts a YouTube video's transcript, chunks it, creates embeddings, stores those in a FAISS index, and lets you ask questions or generate summaries using a language model (GROQ or OpenAI).

Quick summary

- Input: YouTube URL
- Output: Study summary, interview questions, downloadable PDF, and a QA interface

Features

- Fetch YouTube transcripts (via `youtube-transcript-api`)
- Split transcript into chunks
- Create embeddings (`sentence-transformers` locally)
- Store embeddings in FAISS
- Answer questions using a language model (GROQ or OpenAI)
- Generate study summaries and interview Q&A
- Export PDF notes

Prerequisites

- Python 3.10+ (3.12 recommended)
- Git (if you want to push to GitHub)

Install

1. Create a virtual environment (optional but recommended):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install Python dependencies:

```powershell
py -m pip install -r requirements.txt
```

3. (Optional) Install `langchain-groq` if you plan to use GROQ:

```powershell
py -m pip install langchain-groq
```

Environment variables

Copy the example env file and fill your keys locally (do not commit):

```powershell
copy .env.example .env
# then edit .env and add your keys
```

- `GROQ_API_KEY` — your GROQ API key (optional)
- `OPENAI_API_KEY` — your OpenAI API key (optional fallback)

The repo keeps only `.env.example` with empty placeholders. Add your real
keys to `.env` locally and never commit that file.

Quick setup (Windows PowerShell):

```powershell
.\scripts\install.ps1
.\scripts\run.ps1
```

Quick setup (Linux / macOS):

```bash
./scripts/install.sh
./scripts/run.sh
```
 
 Note: the repo intentionally keeps these placeholders empty. Do NOT commit
 real keys. If both keys are empty the application will still run, but LLM
 responses will be replaced with guidance text until you provide a valid key.

 Example `.env` (keep keys empty in the repository):

 ```
 # .env - local development secrets (DO NOT COMMIT REAL KEYS)
 GROQ_API_KEY=
 OPENAI_API_KEY=
 ```

 How to set keys locally (PowerShell):

 ```powershell
 $env:OPENAI_API_KEY = 'sk_...'
 #or add to your local .env file (do not commit)
 ```

 How to set keys locally (Linux / macOS):

 ```bash
 export OPENAI_API_KEY="sk_..."
 ```

Run the app

```powershell
py -m streamlit run app.py
```

Or run the pipeline script (headless) on the sample video:

```powershell
py run_video.py
```

Files in this repo

- `app.py` — Streamlit UI
- `rag_backend.py` — core functions: transcript fetch, chunking, embeddings, FAISS store, LLM calls
- `run_video.py` — small runner to process a single video from the command line
- `requirements.txt` — dependency list
- `.env` — local environment placeholders (do not commit secrets)
- `.gitignore` — ignore patterns
- `summary.txt`, `interview_questions.txt` — generated outputs (created when run)

How it works (simple flow)

1. User pastes a YouTube URL in the UI.
2. The app fetches the transcript using `youtube-transcript-api`.
3. Transcript is split into chunks (default chunk size ~1000 chars).
4. Each chunk is embedded using `sentence-transformers` (local model).
5. Embeddings are stored in a FAISS vector index.
6. For questions, the app retrieves similar chunks from FAISS and sends them + the question to the LLM.
7. The LLM returns an answer, summary, or interview Q&A.

Notes and troubleshooting (common issues)

- Transformers / TF errors: Local `sentence-transformers` may import `transformers` which in turn can require TensorFlow compatibility. If you see an error complaining about Keras 3, install `tf-keras`:

```powershell
py -m pip install tf-keras
```

	Installing TF can upgrade/downgrade other packages (protobuf, tensorflow). If you want to avoid heavy local installs, use a hosted embedding service instead of local `sentence-transformers`.

- `ModuleNotFoundError` for `youtube_transcript_api`:

```powershell
py -m pip install youtube-transcript-api
```

- Streamlit not found: run via module if `streamlit` script isn't on PATH:

```powershell
py -m streamlit run app.py
```

Security

- Never commit real API keys. Keep `.env` out of source control (it is in `.gitignore`). Use GitHub secrets or cloud secret stores for CI/deploy.

Development notes

- `rag_backend.py` lazily imports heavy ML libraries inside `create_vector_db()` to avoid import-time crashes when those dependencies are not installed.
- The project prefers `ChatGroq` when `GROQ_API_KEY` is set and falls back to OpenAI otherwise.

Recommended next steps

- Pin dependency versions in `requirements.txt` (to make installs reproducible)
- Add a simple GitHub Action to run `py -m pip install -r requirements.txt` and `py -c "import rag_backend"` to catch import errors on CI.
- Replace local embeddings with a hosted embedding API to reduce heavy local installs.

Contributing

- Open an issue or create a PR. Keep changes focused. Run tests (if added) and lint before submitting.

License & contact

- This repo has no license file by default — add one if you plan to publish. Add `LICENSE` with MIT/Apache/other.
- Contact: use your GitHub profile or add an `OWNER` file.
