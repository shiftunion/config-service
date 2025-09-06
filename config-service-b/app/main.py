"""
Main FastAPI application.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.applications import router as applications_router
from app.api.routes.configurations import router as configurations_router
from app.core.config import get_settings, setup_logging
from app.db.pool import close_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    settings = get_settings()
    setup_logging(settings.log_level)

    yield

    # Shutdown
    close_pool()


app = FastAPI(
    title="Config Service API",
    description="REST API for managing applications and their configurations",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers with /api/v1 prefix
app.include_router(
    applications_router,
    prefix="/api/v1",
    tags=["applications"]
)

app.include_router(
    configurations_router,
    prefix="/api/v1",
    tags=["configurations"]
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
