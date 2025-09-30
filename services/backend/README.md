Backend service (FastAPI)

*local poetry*:

```bash
poetry install

MEILI_API_KEY=tiMpun-mipvy5-tehxiw \
poetry run uvicorn src.api.main:app --host 0.0.0.0 --port 8000  --reload
```