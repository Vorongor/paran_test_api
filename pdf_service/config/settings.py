from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PDFSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    BASE_DIR: Path = Path(__file__).parent.parent
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

    AWS_ENDPOINT_URL: str = Field(
        "http://localstack:4566", alias="AWS_ENDPOINT_URL"
    )
    AWS_ACCESS_KEY_ID: str = Field("test", alias="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field("test", alias="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field("us-east-1", alias="AWS_REGION")

    SQS_QUEUE_NAME: str = Field("pdf-jobs")
    S3_BUCKET_NAME: str = Field("user-pdfs")

