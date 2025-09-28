#!/usr/bin/env bash
set -euo pipefail
# Start the FastAPI backend using the project's conda Python and ensure PYTHONPATH is set
#
# Usage examples:
# 1) Start backend with defaults:
#    ./scripts/start-backend.sh
#
# 2) Override python executable (useful if not using repo .conda):
#    PYTHON_PATH="/usr/bin/python3" ./scripts/start-backend.sh
#
# 3) Run with a custom Meilisearch API key (export or inline):
#    MEILI_API_KEY="tiMpun-mipvy5-tehxiw" ./scripts/start-backend.sh
#
# Notes:
#  - The script sets `PYTHONPATH=services/backend` so `src` is importable when running uvicorn.
#  - Use `--host 0.0.0.0 --port 8000` are set by the script; edit the script if you need custom arguments.
#

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Default python inside the project's conda env — override with PYTHON env var if needed
PYTHON_PATH="${PYTHON_PATH:-$REPO_ROOT/.conda/bin/python}"

export PYTHONPATH="${PYTHONPATH:-services/backend}"
export MEILI_API_KEY="${MEILI_API_KEY:-tiMpun-mipvy5-tehxiw}"

echo "Starting backend with python: $PYTHON_PATH"
echo "PYTHONPATH=$PYTHONPATH"

exec "$PYTHON_PATH" -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
