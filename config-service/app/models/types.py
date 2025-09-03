from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel, Field
from pydantic_extra_types.ulid import ULID


class AppBase(BaseModel):
    name: str = Field(min_length=1, max_length=256)
    comments: str | None = Field(default=None, max_length=1024)


class ApplicationCreate(AppBase):
    id: ULID


class ApplicationUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=256)
    comments: str | None = Field(default=None, max_length=1024)


class ApplicationOut(AppBase):
    id: ULID
    configuration_ids: list[str] = Field(default_factory=list)


class ConfigBase(BaseModel):
    name: str = Field(min_length=1, max_length=256)
    comments: str | None = Field(default=None, max_length=1024)
    config: Dict[str, Any]


class ConfigurationCreate(ConfigBase):
    id: ULID
    application_id: ULID


class ConfigurationUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=256)
    comments: str | None = Field(default=None, max_length=1024)
    config: Dict[str, Any] | None = None


class ConfigurationOut(ConfigBase):
    id: ULID
    application_id: ULID
