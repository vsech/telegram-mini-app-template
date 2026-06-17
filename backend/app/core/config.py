from functools import lru_cache

from pydantic import AnyHttpUrl, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "telegram-mini-app-template"
    ENVIRONMENT: str = "local"
    DEBUG: bool = True

    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost"

    POSTGRES_DB: str = "telegram_app"
    POSTGRES_USER: str = "telegram_app"
    POSTGRES_PASSWORD: str = "telegram_app"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str = (
        "postgresql+psycopg://telegram_app:telegram_app@db:5432/telegram_app"
    )

    TELEGRAM_BOT_TOKEN: str = "change-me"
    TELEGRAM_INIT_DATA_TTL_SECONDS: int = 24 * 60 * 60
    FRONTEND_URL: AnyHttpUrl | str = "http://localhost:5173"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.BACKEND_CORS_ORIGINS.split(",")
            if origin.strip()
        ]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def async_database_url(self) -> str:
        if self.DATABASE_URL.startswith("postgresql://"):
            return self.DATABASE_URL.replace(
                "postgresql://",
                "postgresql+psycopg://",
                1,
            )
        return self.DATABASE_URL


@lru_cache
def get_settings() -> Settings:
    return Settings()
