# Architecture Overview

Simple overview of components:

- `services/scraper`: scrapes websites, parses and normalises events, writes `concert_events_*.json`.
- `services/backend`: FastAPI service that provides indexing and search endpoints and a Meilisearch wrapper.
- `services/frontend`: React (Vite) app that offers search UI and filters.
- `data.ms/`: Meilisearch local DB (persistent). Do not delete.
