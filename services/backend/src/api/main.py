from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import search


def create_app():
    app = FastAPI(title="gigfusion-backend")

    # Development CORS - allow local frontend origins used by Vite dev server
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(search.router)
    return app


app = create_app()
