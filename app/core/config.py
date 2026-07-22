from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "VisionAuth"
    app_version: str = "0.1.0"

    environment: str = "development"

    debug: bool = True

    api_v1_prefix: str = "/api/v1"

    host: str = "localhost"

    port: int = 8000

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "visionauth"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"

    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/visionauth"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


settings = get_settings()
