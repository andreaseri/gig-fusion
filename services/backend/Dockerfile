### Multi-stage build using Poetry for dependency resolution
### Builder stage: export pinned requirements and install into /install
FROM python:3.13-slim-bookworm AS builder

WORKDIR /build

# System deps commonly needed for building wheels; adjust if necessary
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	&& rm -rf /var/lib/apt/lists/*

# Install Poetry and disable virtualenv creation so it installs into system Python
RUN pip install --no-cache-dir "poetry>=1.8.3" && \
    poetry self add poetry-plugin-export && \
	poetry config virtualenvs.create false

# Copy project metadata (lockfile preferred) and export pinned requirements
COPY pyproject.toml poetry.lock /build/

RUN poetry export --without-hashes -f requirements.txt -o requirements.txt --all-extras

# Install runtime dependencies into an isolated prefix so we can copy them into final image
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir --prefix=/install --ignore-installed -r requirements.txt


### Runtime image
FROM python:3.13-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy app source
COPY src/ /app/

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
