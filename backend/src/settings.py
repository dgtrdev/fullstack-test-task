from pathlib import Path

from pydantic import AliasChoices, Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore",
    )

    postgres_user: str = Field(validation_alias="POSTGRES_USER")
    postgres_password: str = Field(validation_alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(validation_alias="POSTGRES_HOST")
    postgres_port: int = Field(validation_alias="PGPORT")
    postgres_db: str = Field(validation_alias="POSTGRES_DB")
    redis_url: str = Field(
        default="redis://backend-redis:6379/0",
        validation_alias=AliasChoices("REDIS_URL", "CELERY_BROKER_URL"),
    )
    cors_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        validation_alias="CORS_ORIGINS",
    )
    storage_dir: Path = Field(
        default=BASE_DIR / "storage" / "files",
        validation_alias="STORAGE_DIR",
    )

    @field_validator("storage_dir", mode="after")
    @classmethod
    def resolve_storage_dir(cls, value: Path) -> Path:
        if value.is_absolute():
            return value

        return BASE_DIR / value

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

settings = Settings()
