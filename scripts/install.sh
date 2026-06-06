#!/usr/bin/env bash
# Shell helper: create venv and install requirements
set -e
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo "Dependencies installed. Activate with 'source .venv/bin/activate' and run './scripts/run.sh'"
