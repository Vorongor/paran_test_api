from pathlib import Path

from pydantic import computed_field, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import StaticPool


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

    SECRET_KEY_ACCESS: str = Field(
        "placeholder_access", alias="SECRET_KEY_ACCESS"
    )
    SECRET_KEY_REFRESH: str = Field(
        "placeholder_refresh", alias="SECRET_KEY_REFRESH"
    )
    JWT_SIGNING_ALGORITHM: str = "HS256"

    @property
    def DATABASE_URL(self) -> str:
        return f"sqlite+aiosqlite:///{self.BASE_DIR}/project_db.db"


class Settings(BaseAppSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB_PORT: int = 5432
    POSTGRES_DB: str

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


class TestingSettings(BaseAppSettings):
    """TEST_SETTINGS: SQLite in-memory"""

    ENVIRONMENT: str = "test"
    SECRET_KEY_ACCESS: str = "test_secret"
    SECRET_KEY_REFRESH: str = "test_secret"

    DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"

    ENGINE_KWARGS: dict = {
        "poolclass": StaticPool,
        "connect_args": {"check_same_thread": False},
    }
