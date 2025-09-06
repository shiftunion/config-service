"""
Applications API routes.
"""
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic_extra_types.ulid import ULID

from app.models.types import Application, ApplicationCreate
from app.services.applications_service import ApplicationsService

router = APIRouter()


@router.post("/applications", response_model=Application)
async def create_application(application: ApplicationCreate):
    """Create new application."""
    return await ApplicationsService.create(application)


@router.put("/applications/{application_id}", response_model=Application)
async def update_application(application_id: str, application: ApplicationCreate):
    """Update application."""
    try:
        ULID(application_id)  # Validate ULID format
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ULID format")

    return await ApplicationsService.update(application_id, application)


@router.get("/applications/{application_id}")
async def get_application(application_id: str):
    """Get application by ID."""
    try:
        ULID(application_id)  # Validate ULID format
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ULID format")

    return await ApplicationsService.get_by_id(application_id)


@router.get("/applications", response_model=List[Application])
async def get_applications():
    """Get all applications."""
    return await ApplicationsService.get_all()
