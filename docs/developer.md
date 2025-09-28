# Developer Quickstart

1. Create the conda env:

```bash
conda env create -f environment.yml
conda activate eventing
```

2. Start Meilisearch (dev):

```bash
docker run --rm -it -p 7700:7700 \
  -v "$PWD/data/data.ms:/data.ms" \
  -e MEILI_MASTER_KEY="<your-key>" \
  getmeili/meilisearch:latest \
  meilisearch --db-path /data.ms --master-key "$MEILI_MASTER_KEY"
```

3. Use `infra/docker-compose.dev.yml` to start backend/frontend locally (after building images).
