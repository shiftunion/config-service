from __future__ import annotations

"""Applications API routes."""

from fastapi import APIRouter, Depends

from app.api.deps import get_pool
from app.models.types import ApplicationCreate, ApplicationOut, ApplicationUpdate
from app.services.applications_service import ApplicationsService


router = APIRouter(prefix="/applications", tags=["applications"])


def service():
    """Dependency factory returning an `ApplicationsService`."""
    return ApplicationsService(get_pool())


@router.post("", response_model=ApplicationOut, status_code=201)
def create_application(data: ApplicationCreate, svc: ApplicationsService = Depends(service)):
    """Create a new application."""
    return svc.create(data)


@router.put("/{id}", response_model=ApplicationOut)
def update_application(id: str, data: ApplicationUpdate, svc: ApplicationsService = Depends(service)):
    """Update an application by id."""
    return svc.update(str(id), data)


@router.get("/{id}", response_model=ApplicationOut)
def get_application(id: str, svc: ApplicationsService = Depends(service)):
    """Fetch an application by id."""
    return svc.get(str(id))


@router.get("", response_model=list[ApplicationOut])
def list_applications(svc: ApplicationsService = Depends(service)):
    """List applications with their configuration ids."""
    return svc.list()
