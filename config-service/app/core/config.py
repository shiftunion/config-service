from __future__ import annotations

import logging
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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
        return getattr(logging, self.LOG_LEVEL.upper(), logging.INFO)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    s = Settings()
    logging.basicConfig(level=s.log_level(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    return s
