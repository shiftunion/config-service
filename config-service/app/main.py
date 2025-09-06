from __future__ import annotations

"""Application entrypoint and FastAPI setup."""

import logging
from fastapi import FastAPI

from app.api.routes.applications import router as applications_router
from app.api.routes.configurations import router as configurations_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(title="Config Service", version="0.1.0")

    app.include_router(applications_router, prefix="/api/v1")
    app.include_router(configurations_router, prefix="/api/v1")

    return app


app = create_app()

# configure root logger level via settings during startup in deps
logging.getLogger("uvicorn").setLevel(logging.INFO)
