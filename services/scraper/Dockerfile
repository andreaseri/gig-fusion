FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev
COPY src/ /app/src/
COPY services/scraper/scripts/ /app/scripts/
ENV PYTHONPATH=/app/src
CMD ["python", "/app/scripts/run_scraper.py"]
