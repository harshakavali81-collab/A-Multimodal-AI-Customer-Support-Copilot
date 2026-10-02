#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then python3 -m venv .venv; fi
.venv/bin/python -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
.venv/bin/python -m pip install -r requirements-models.txt
.venv/bin/python scripts/download_models.py
export LLM_BACKEND=transformers
export SEMANTIC_SEARCH=1
exec .venv/bin/python app.py
