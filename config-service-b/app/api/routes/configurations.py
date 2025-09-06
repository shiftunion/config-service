"""
Configurations API routes.
"""
from fastapi import APIRouter, HTTPException
from pydantic_extra_types.ulid import ULID

from app.models.types import Configuration, ConfigurationCreate
from app.services.configurations_service import ConfigurationsService

router = APIRouter()


@router.post("/configurations", response_model=Configuration)
async def create_configuration(configuration: ConfigurationCreate):
    """Create new configuration."""
    return await ConfigurationsService.create(configuration)


@router.put("/configurations/{configuration_id}", response_model=Configuration)
async def update_configuration(configuration_id: str, updates: ConfigurationCreate):
    """Update configuration."""
    try:
        ULID(configuration_id)  # Validate ULID format
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ULID format")

    return await ConfigurationsService.update(configuration_id, updates)


@router.get("/configurations/{configuration_id}", response_model=Configuration)
async def get_configuration(configuration_id: str):
    """Get configuration by ID."""
    try:
        ULID(configuration_id)  # Validate ULID format
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ULID format")

    return await ConfigurationsService.get_by_id(configuration_id)
