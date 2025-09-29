# gigfunsion (monorepo)

Monorepo for scraping, parsing, indexing into Meilisearch, serving via FastAPI and a React frontend.

See `docs/` for architecture and developer notes. Use `infra/docker-compose.dev.yml` for local development.


```bash
PYTHONPATH=services/backend \
MEILI_API_KEY=tiMpun-mipvy5-tehxiw \
/Users/andreaseri/Development/projects/andreas/eventing/.conda/bin/python -m uvicorn src.api.main:app \
  --host 0.0.0.0 --port 8000 --reload
```

```bash
cd /Users/andreaseri/Development/projects/andreas/eventing/services/frontend
npm run dev
```

```bash
SCRAPER_OUTPUT_DIR="data/raw/underdog" ./scripts/start-parse.sh
```

```bash
API_KEY="tiMpun-mipvy5-tehxiw" ./scripts/start-reindex.sh --path data/raw/underdog
```

```bash
docker run -it \     
  -p 7700:7700 \
  -e MEILI_MASTER_KEY="tiMpun-mipvy5-tehxiw" \ 
  getmeili/meilisearch:latest
```
