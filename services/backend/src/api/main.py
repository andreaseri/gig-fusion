from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import search
import os


def create_app():
    app = FastAPI(title="gigfusion-backend")

    # Load CORS settings from environment variables
    origins = os.getenv("CORS_ALLOW_ORIGINS", "*")
    methods = os.getenv("CORS_ALLOW_METHODS", "GET,POST,PUT,DELETE,OPTIONS")
    headers = os.getenv("CORS_ALLOW_HEADERS", "*")
    credentials = os.getenv("CORS_ALLOW_CREDENTIALS", "false")

    # Convert to proper types
    if origins != "*":
        origins = [o.strip() for o in origins.split(",")]
    else:
        origins = ["*"]

    methods = [m.strip() for m in methods.split(",")]
    headers = [h.strip() for h in headers.split(",")]
    credentials = credentials.lower() == "true"

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=credentials,
        allow_methods=methods,
        allow_headers=headers,
    )

    app.include_router(search.router)
    return app


app = create_app()
