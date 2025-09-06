"""
Type definitions and Pydantic models.
"""
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_extra_types.ulid import ULID


class ApplicationBase(BaseModel):
    """Base application model."""
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., max_length=256)
    comments: str = Field("", max_length=1024)


class ApplicationCreate(ApplicationBase):
    """Application creation model."""
    pass


class ApplicationUpdate(ApplicationBase):
    """Application update model."""
    pass


class Application(ApplicationBase):
    """Full application model."""
    id: ULID

    @field_validator('id', mode='before')
    @classmethod
    def validate_ulid(cls, v):
        """Validate ULID format."""
        if isinstance(v, str):
            return ULID(v)
        return v


class ConfigurationBase(BaseModel):
    """Base configuration model."""
    model_config = ConfigDict(from_attributes=True)

    application_id: ULID
    name: str = Field(..., max_length=256)
    comments: str = Field("", max_length=1024)
    config: Dict[str, Any]

    @field_validator('application_id', mode='before')
    @classmethod
    def validate_application_id(cls, v):
        """Validate application_id ULID format."""
        if isinstance(v, str):
            return ULID(v)
        return v


class ConfigurationCreate(ConfigurationBase):
    """Configuration creation model."""
    pass


class ConfigurationUpdate(BaseModel):
    """Configuration update model."""
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., max_length=256)
    comments: str = Field("", max_length=1024)
    config: Dict[str, Any]


class Configuration(ConfigurationBase):
    """Full configuration model."""
    id: ULID

    @field_validator('id', mode='before')
    @classmethod
    def validate_ulid(cls, v):
        """Validate ULID format."""
        if isinstance(v, str):
            return ULID(v)
        return v


class ApplicationWithConfigIds(Application):
    """Application with related configuration IDs."""
    configuration_ids: list[ULID] = Field(default_factory=list)
