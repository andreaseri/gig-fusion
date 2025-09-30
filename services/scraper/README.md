Scraper service

Run `python scripts/run_scraper.py` to fetch, parse and write `concert_events_*.json`.

```bash
VERSION=v0.1.0
docker buildx build --progress plain --no-cache \
  --platform linux/amd64,linux/arm64 \
  -t andreaseri/gig-fusion-scraper:${VERSION} \
  -f services/scraper/Dockerfile \
  services/scraper \
  --load
```

```bash
docker run -it --network gigfusion -e MEILI_URL="http://meilisearch:7700" -e MEILI_API_KEY="tiMpun-mipvy5-tehxiw" andreaseri/gig-fusion-scraper:v0.1.0
```