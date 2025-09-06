from __future__ import annotations

"""Runtime application settings.

Settings are sourced from environment variables (optionally via a local
`.env` file). Use `get_settings()` for a cached, configured `Settings`
instance and to initialize logging with the configured level.
"""

import logging
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed application configuration loaded from the environment."""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_ENV: str = "dev"
    LOG_LEVEL: str = "INFO"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "configsvc"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    DB_POOL_MIN: int = 1
    DB_POOL_MAX: int = 10

    def log_level(self) -> int:
        """Return the numeric log level derived from `LOG_LEVEL`."""
        return getattr(logging, self.LOG_LEVEL.upper(), logging.INFO)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached `Settings` and configure root logging once.

    The first call sets up `logging.basicConfig` using the configured level.
    Subsequent calls return the cached instance.
    """
    s = Settings()
    logging.basicConfig(level=s.log_level(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    return s
