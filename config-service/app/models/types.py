from __future__ import annotations

"""Pydantic models for API requests and responses."""

from typing import Any, Dict

from pydantic import BaseModel, Field


class AppBase(BaseModel):
    """Common fields for application models."""

    name: str = Field(min_length=1, max_length=256)
    comments: str | None = Field(default=None, max_length=1024)


class ApplicationCreate(AppBase):
    """Payload for creating an application."""

    id: str


class ApplicationUpdate(BaseModel):
    """Partial update payload for an application."""

    name: str | None = Field(default=None, max_length=256)
    comments: str | None = Field(default=None, max_length=1024)


class ApplicationOut(AppBase):
    """Application response model with related configuration ids."""

    id: str
    configuration_ids: list[str] = Field(default_factory=list)


class ConfigBase(BaseModel):
    """Common fields for configuration models."""

    name: str = Field(min_length=1, max_length=256)
    comments: str | None = Field(default=None, max_length=1024)
    config: Dict[str, Any]


class ConfigurationCreate(ConfigBase):
    """Payload for creating a configuration for an application."""

    id: str
    application_id: str


class ConfigurationUpdate(BaseModel):
    """Partial update payload for a configuration."""

    name: str | None = Field(default=None, max_length=256)
    comments: str | None = Field(default=None, max_length=1024)
    config: Dict[str, Any] | None = None


class ConfigurationOut(ConfigBase):
    """Configuration response model."""

    id: str
    application_id: str
