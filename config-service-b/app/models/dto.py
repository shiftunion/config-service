"""
Data Transfer Objects for API requests and responses.
"""
from typing import Any, Dict, List

from pydantic_extra_types.ulid import ULID

from .types import Application, ApplicationWithConfigIds, Configuration


# Response DTOs
ApplicationResponse = Application
ConfigurationResponse = Configuration
ApplicationWithConfigIdsResponse = ApplicationWithConfigIds


# Request DTOs - reuse from types for simplicity
class CreateApplicationRequest:
    """Create application request."""
    def __init__(self, name: str, comments: str = ""):
        self.name = name
        self.comments = comments


class UpdateApplicationRequest:
    """Update application request."""
    def __init__(self, name: str, comments: str = ""):
        self.name = name
        self.comments = comments


class CreateConfigurationRequest:
    """Create configuration request."""
    def __init__(self, application_id: ULID, name: str, comments: str = "", config: Dict[str, Any] = None):
        self.application_id = application_id
        self.name = name
        self.comments = comments
        self.config = config or {}


class UpdateConfigurationRequest:
    """Update configuration request."""
    def __init__(self, name: str, comments: str = "", config: Dict[str, Any] = None):
        self.name = name
        self.comments = comments
        self.config = config or {}


# Collections
ApplicationsResponse = List[ApplicationResponse]
ConfigurationsResponse = List[ConfigurationResponse]
