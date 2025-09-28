FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev
COPY src/ /app/src/
ENV PYTHONPATH=/app/src
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
