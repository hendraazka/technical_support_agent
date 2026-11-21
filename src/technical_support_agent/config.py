"""Application settings loaded from environment variables."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration. Environment variables use the TSA_ prefix."""

    model_config = SettingsConfigDict(env_prefix="TSA_", env_file=".env", extra="ignore")

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    log_json: bool = False
    ollama_base_url: str = "http://localhost:11434"
    docker_host: str = "tcp://127.0.0.1:12375"


@lru_cache
def get_settings() -> Settings:
    """Return the cached settings instance."""
    return Settings()
