#!/usr/bin/env bash
set -euo pipefail

# Top-level ingest wrapper — runs the repository-level ingest script
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_PATH="${PYTHON_PATH:-$REPO_ROOT/.conda/bin/python}"
INGEST_SCRIPT="$REPO_ROOT/scripts/ingest_meilis.py"

if [ ! -f "$INGEST_SCRIPT" ]; then
  echo "Ingest script not found at $INGEST_SCRIPT"
  exit 2
fi

echo "Running ingest with python: $PYTHON_PATH"
exec "$PYTHON_PATH" "$INGEST_SCRIPT" "$@"
