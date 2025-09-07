from __future__ import annotations

"""Application entrypoint and FastAPI setup."""

import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.applications import router as applications_router
from app.api.routes.configurations import router as configurations_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(title="Config Service", version="0.1.0")

    # CORS configuration via env var CORS_ORIGINS (comma-separated)
    # Examples:
    #  - CORS_ORIGINS=http://localhost:5173
    #  - CORS_ORIGINS=https://admin.example.com,https://admin.staging.example.com
    #  - CORS_ORIGINS=*   (credentials disabled automatically)
    raw = os.getenv("CORS_ORIGINS", "http://localhost:5173").strip()
    origins = [o.strip() for o in raw.split(",") if o.strip()] if raw != "*" else ["*"]
    allow_credentials = raw != "*"  # wildcard cannot be used with credentials=true per spec

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(applications_router, prefix="/api/v1")
    app.include_router(configurations_router, prefix="/api/v1")

    return app


app = create_app()

# configure root logger level via settings during startup in deps
logging.getLogger("uvicorn").setLevel(logging.INFO)
