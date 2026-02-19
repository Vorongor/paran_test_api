import os
from typing import Optional
from pathlib import Path

from pydantic import computed_field, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    BASE_DIR: Path = Path(__file__).parent.parent
    ENVIRONMENT: str = "local"
    API_V1_PREFIX: str = "/api/v1"

    REFRESH_TOKEN_DAYS: int = 7
    ACCESS_KEY_TIMEDELTA_MINUTES: int = 60

    SECRET_KEY_ACCESS: str = "placeholder_access"
    SECRET_KEY_REFRESH: str = "placeholder_refresh"
    JWT_SIGNING_ALGORITHM: str = "HS256"

    @property
    def DATABASE_URL(self) -> str:
        return f"sqlite+aiosqlite:///{self.BASE_DIR}/project_db.db"


class Settings(BaseAppSettings):
    POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: Optional[str] = os.getenv("POSTGRES_HOST")
    POSTGRES_DB_PORT: int = 5432
    POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB")

    SECRET_KEY_ACCESS: str = Field(
        default_factory=lambda: os.getenv(
            "SECRET_KEY_ACCESS", os.urandom(32).hex()
        )
    )
    SECRET_KEY_REFRESH: str = Field(
        default_factory=lambda: os.getenv(
            "SECRET_KEY_REFRESH", os.urandom(32).hex()
        )
    )
    JWT_SIGNING_ALGORITHM: str = "HS256"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}"
            f":{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}"
            f":{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB}"
        )


class LocalSettings(BaseAppSettings):
    """DEV_SETTINGS: Local SQLite"""

    ENVIRONMENT: str = "local"

    @property
    def DATABASE_URL(self) -> str:
        return "sqlite+aiosqlite:///project_db.db"


class TestingSettings(BaseAppSettings):
    """TEST_SETTINGS: SQLite in-memory"""

    ENVIRONMENT: str = "test"

    SECRET_KEY_ACCESS: str = "test_secret"
    SECRET_KEY_REFRESH: str = "test_secret"
    JWT_SIGNING_ALGORITHM: str = "HS256"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return "sqlite+aiosqlite:///:memory:"

    @computed_field
    @property
    def PATH_TO_MOVIES_CSV(self) -> str:
        return str(self.BASE_DIR / "database" / "seed_data" / "test_data.csv")
