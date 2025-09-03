from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic_extra_types.ulid import ULID

from app.api.deps import get_pool
from app.models.types import ApplicationCreate, ApplicationOut, ApplicationUpdate
from app.services.applications_service import ApplicationsService


router = APIRouter(prefix="/applications", tags=["applications"])


def service():
    return ApplicationsService(get_pool())


@router.post("", response_model=ApplicationOut, status_code=201)
def create_application(data: ApplicationCreate, svc: ApplicationsService = Depends(service)):
    return svc.create(data)


@router.put("/{id}", response_model=ApplicationOut)
def update_application(id: ULID, data: ApplicationUpdate, svc: ApplicationsService = Depends(service)):
    return svc.update(str(id), data)


@router.get("/{id}", response_model=ApplicationOut)
def get_application(id: ULID, svc: ApplicationsService = Depends(service)):
    return svc.get(str(id))


@router.get("", response_model=list[ApplicationOut])
def list_applications(svc: ApplicationsService = Depends(service)):
    return svc.list()
