"""
Application configuration.
"""
import logging
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "config_service"
    db_user: str = "config_user"
    db_password: str = "config_pass"

    # Connection Pool Settings
    db_pool_min_conn: int = 1
    db_pool_max_conn: int = 10

    # Application Settings
    log_level: str = "INFO"

    # Development Settings
    uvicorn_host: str = "0.0.0.0"
    uvicorn_port: int = 8000

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()


def setup_logging(log_level: str = "INFO"):
    """Setup application logging."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
