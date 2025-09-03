from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic_extra_types.ulid import ULID

from app.api.deps import get_pool
from app.models.types import ConfigurationCreate, ConfigurationOut, ConfigurationUpdate
from app.services.configurations_service import ConfigurationsService


router = APIRouter(prefix="/configurations", tags=["configurations"])


def service():
    return ConfigurationsService(get_pool())


@router.post("", response_model=ConfigurationOut, status_code=201)
def create_configuration(data: ConfigurationCreate, svc: ConfigurationsService = Depends(service)):
    return svc.create(data)


@router.put("/{id}", response_model=ConfigurationOut)
def update_configuration(id: ULID, data: ConfigurationUpdate, svc: ConfigurationsService = Depends(service)):
    return svc.update(str(id), data)


@router.get("/{id}", response_model=ConfigurationOut)
def get_configuration(id: ULID, svc: ConfigurationsService = Depends(service)):
    return svc.get(str(id))
