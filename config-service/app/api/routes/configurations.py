from __future__ import annotations

"""Configurations API routes."""

from fastapi import APIRouter, Depends

from app.api.deps import get_pool
from app.models.types import ConfigurationCreate, ConfigurationOut, ConfigurationUpdate
from app.services.configurations_service import ConfigurationsService


router = APIRouter(prefix="/configurations", tags=["configurations"])


def service():
    """Dependency factory returning a `ConfigurationsService`."""
    return ConfigurationsService(get_pool())


@router.post("", response_model=ConfigurationOut, status_code=201)
def create_configuration(data: ConfigurationCreate, svc: ConfigurationsService = Depends(service)):
    """Create a configuration for an application."""
    return svc.create(data)


@router.put("/{id}", response_model=ConfigurationOut)
def update_configuration(id: str, data: ConfigurationUpdate, svc: ConfigurationsService = Depends(service)):
    """Update a configuration by id."""
    return svc.update(str(id), data)


@router.get("/{id}", response_model=ConfigurationOut)
def get_configuration(id: str, svc: ConfigurationsService = Depends(service)):
    """Fetch a configuration by id."""
    return svc.get(str(id))
