#!/usr/bin/env bash
if [ ! -d ".venv" ]; then
  echo "Virtual environment not found. Run ./scripts/install.sh first." >&2
  exit 1
fi
source .venv/bin/activate
python -m streamlit run app.py
