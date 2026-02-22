from typing import Annotated

from fastapi import Depends

from pdf_service.config import PDFSettings
from pdf_service.storage.interfaces import SQSStorageInterface
from pdf_service.storage.s3 import S3StorageClient
from pdf_service.storage.sqs import SQSClient


# from pdf_service.security import JWTAuthManager


def get_settings() -> PDFSettings:
    """
    Retrieve the application settings based on the current environment.
    """
    return PDFSettings()


async def get_s3_manager(
    settings: Annotated[PDFSettings, Depends(get_settings)]
) -> S3StorageClient:
    return S3StorageClient(
        endpoint_url=settings.AWS_ENDPOINT_URL,
        access_key=settings.AWS_ACCESS_KEY_ID,
        secret_key=settings.AWS_SECRET_ACCESS_KEY,
        bucket_name=settings.S3_BUCKET_NAME,
        region_name=settings.AWS_REGION,
    )


async def get_sqs_manager(
    settings: Annotated[PDFSettings, Depends(get_settings)]
) -> SQSStorageInterface:
    return SQSClient(
        endpoint_url=settings.AWS_ENDPOINT_URL,
        access_key=settings.AWS_ACCESS_KEY_ID,
        secret_key=settings.AWS_SECRET_ACCESS_KEY,
        queue_name=settings.SQS_QUEUE_NAME,
        region_name=settings.AWS_REGION,
    )


# def get_jwt_manager(
#     settings: Annotated[Settings, Depends(get_settings)],
# ) -> JWTAuthManager:
#     """
#     Create and return a JWT authentication manager instance.
#     """
#     return JWTAuthManager(
#         secret_key_access=settings.SECRET_KEY_ACCESS,
#         secret_key_refresh=settings.SECRET_KEY_REFRESH,
#         algorithm=settings.JWT_SIGNING_ALGORITHM,
#     )
#
#
# SettingsDep = Annotated[Settings, Depends(get_settings)]
# JWTManagerDep = Annotated[JWTAuthManager, Depends(get_jwt_manager)]
