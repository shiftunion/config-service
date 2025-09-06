"""
Applications service for business logic.
"""
from typing import List, Optional

from fastapi import HTTPException

from app.models.types import Application, ApplicationCreate, ApplicationWithConfigIds
from app.repositories.applications_repo import ApplicationsRepository
from app.repositories.configurations_repo import ConfigurationsRepository

from pydantic_extra_types.ulid import ULID


class ApplicationsService:
    """Service for applications business logic."""

    @staticmethod
    async def get_all() -> List[Application]:
        """Get all applications."""
        return await ApplicationsRepository.get_all()

    @staticmethod
    async def get_by_id(application_id: str) -> ApplicationWithConfigIds:
        """Get application by ID with configuration IDs."""
        application = await ApplicationsRepository.get_by_id(application_id)
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")

        config_ids = await ApplicationsRepository.get_configuration_ids(application_id)

        return ApplicationWithConfigIds(
            id=application.id,
            name=application.name,
            comments=application.comments,
            configuration_ids=[ULID(cid) for cid in config_ids]
        )

    @staticmethod
    async def create(application: ApplicationCreate) -> Application:
        """Create new application."""
        # Check if name already exists
        existing = await ApplicationsRepository.get_by_name(application.name)
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"Application with name '{application.name}' already exists"
            )

        # Generate ULID
        application_id = str(ULID.generate())

        return await ApplicationsRepository.create(application, application_id)

    @staticmethod
    async def update(application_id: str, application: ApplicationCreate) -> Application:
        """Update application."""
        # Check if application exists
        existing_app = await ApplicationsRepository.get_by_id(application_id)
        if not existing_app:
            raise HTTPException(status_code=404, detail="Application not found")

        # Check if name conflicts with another application
        existing_name = await ApplicationsRepository.get_by_name(application.name)
        if existing_name and str(existing_name.id) != application_id:
            raise HTTPException(
                status_code=409,
                detail=f"Application with name '{application.name}' already exists"
            )

        updated = await ApplicationsRepository.update(application_id, application)
        if not updated:
            raise HTTPException(status_code=404, detail="Application not found")

        return updated

    @staticmethod
    async def delete(application_id: str) -> None:
        """Delete application."""
        # Check if application exists
        application = await ApplicationsRepository.get_by_id(application_id)
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")

        # Check if application has configurations
        config_ids = await ApplicationsRepository.get_configuration_ids(application_id)
        if config_ids:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete application with existing configurations"
            )

        success = await ApplicationsRepository.delete(application_id)
        if not success:
            raise HTTPException(status_code=404, detail="Application not found")
