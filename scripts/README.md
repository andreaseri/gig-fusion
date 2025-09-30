# Scripts

This folder contains developer helper scripts to run parsing, reindexing and ingest flows.

Top-level scripts

- `./scripts/start-backend.sh`: start the FastAPI backend (uses `.conda/bin/python` by default). Examples:

  ```bash
  ./scripts/start-backend.sh
  PYTHON_PATH="/usr/bin/python3" ./scripts/start-backend.sh
  MEILI_API_KEY="tiMpun-mipvy5-tehxiw" ./scripts/start-backend.sh
  ```

- `./scripts/start-frontend.sh`: start the Vite frontend. Example:

  ```bash
  ./scripts/start-frontend.sh
  VITE_BACKEND_URL="http://127.0.0.1:8000" ./scripts/start-frontend.sh
  ```

- `./scripts/start-parse.sh`: run the scraper/parser to produce `concert_events_*.json` files. Example:

  ```bash
  ./scripts/start-parse.sh --path "data/raw/underdog"
  ```

- `./scripts/start-reindex.sh`: index the latest or a specific JSON file into Meilisearch. Examples:

  ```bash
  ./scripts/start-reindex.sh --path data/raw/underdog
  ./scripts/start-reindex.sh --file data/raw/underdog/concert_events_20250922_184039.json
  API_KEY="tiMpun-mipvy5-tehxiw" ./scripts/start-reindex.sh --path data/raw/underdog
  ```
  
Notes

- All scripts default to using the repository `.conda/bin/python` where available; override with `PYTHON_PATH`.
- Prefer passing the Meilisearch API key via `API_KEY` or `MEILI_API_KEY` env var rather than editing scripts.
- Ensure a running Meilisearch instance when reindexing/ingesting.
