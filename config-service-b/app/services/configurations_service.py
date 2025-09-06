"""
Configurations service for business logic.
"""
from typing import List

from fastapi import HTTPException

from app.models.types import Configuration, ConfigurationCreate
from app.repositories.applications_repo import ApplicationsRepository
from app.repositories.configurations_repo import ConfigurationsRepository

from pydantic_extra_types.ulid import ULID


class ConfigurationsService:
    """Service for configurations business logic."""

    @staticmethod
    async def get_by_id(configuration_id: str) -> Configuration:
        """Get configuration by ID."""
        configuration = await ConfigurationsRepository.get_by_id(configuration_id)
        if not configuration:
            raise HTTPException(status_code=404, detail="Configuration not found")

        return configuration

    @staticmethod
    async def create(configuration: ConfigurationCreate) -> Configuration:
        """Create new configuration."""
        # Check if application exists
        app_exists = await ApplicationsRepository.exists(str(configuration.application_id))
        if not app_exists:
            raise HTTPException(status_code=400, detail="Application not found")

        # Check if name already exists for this application
        existing = await ConfigurationsRepository.get_by_app_and_name(
            str(configuration.application_id), configuration.name
        )
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Configuration with this name already exists for the application"
            )

        # Generate ULID
        configuration_id = str(ULID.generate())

        return await ConfigurationsRepository.create(configuration, configuration_id)

    @staticmethod
    async def update(configuration_id: str, updates: ConfigurationCreate) -> Configuration:
        """Update configuration."""
        # Check if configuration exists
        existing_config = await ConfigurationsRepository.get_by_id(configuration_id)
        if not existing_config:
            raise HTTPException(status_code=404, detail="Configuration not found")

        # Check if name already exists for this application (excluding current)
        existing = await ConfigurationsRepository.get_by_app_and_name(
            str(existing_config.application_id), updates.name
        )
        if existing and str(existing.id) != configuration_id:
            raise HTTPException(
                status_code=409,
                detail="Configuration with this name already exists for the application"
            )

        # Create update object without application_id
        update_data = ConfigurationCreate(
            application_id=existing_config.application_id,
            name=updates.name,
            comments=updates.comments,
            config=updates.config
        )

        updated = await ConfigurationsRepository.update(configuration_id, update_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Configuration not found")

        return updated

    @staticmethod
    async def delete(configuration_id: str) -> None:
        """Delete configuration."""
        # Check if configuration exists
        configuration = await ConfigurationsRepository.get_by_id(configuration_id)
        if not configuration:
            raise HTTPException(status_code=404, detail="Configuration not found")

        success = await ConfigurationsRepository.delete(configuration_id)
        if not success:
            raise HTTPException(status_code=404, detail="Configuration not found")
