Backend service (FastAPI)

*local poetry*:

```bash
poetry install

MEILI_API_KEY=tiMpun-mipvy5-tehxiw \
poetry run uvicorn src.api.main:app --host 0.0.0.0 --port 8000  --reload
```

```bash
VERSION=v0.1.0
docker buildx build --progress plain --no-cache \
  --platform linux/amd64,linux/arm64 \
  -t andreaseri/gig-fusion-backend:${VERSION} \
  -f services/backend/Dockerfile \
  services/backend \
  --load
```

```bash
docker run -it -p 8000:8000 --network gigfusion -e MEILI_URL="http://meilisearch:7700" -e MEILI_API_KEY="tiMpun-mipvy5-tehxiw" andreaseri/gig-fusion-backend:v0.1.0
```