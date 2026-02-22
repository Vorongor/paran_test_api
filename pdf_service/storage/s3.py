import logging
from typing import Union

import aioboto3

from pdf_service.config.logging_config import setup_logging
from pdf_service.storage.interfaces import S3StorageInterface

setup_logging()
logger = logging.getLogger(__name__)


class S3StorageClient(S3StorageInterface):

    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        region_name: str,
    ):
        self._endpoint_url = endpoint_url
        self._access_key = access_key
        self._secret_key = secret_key
        self._bucket_name = bucket_name
        self._region_name = region_name
        self._session = aioboto3.Session(
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_key,
        )

    @property
    def session(self):
        return self._session

    async def upload_file(
        self, file_name: str, file_data: Union[bytes, bytearray]
    ) -> None:
        try:
            async with self._session.client(
                "s3", endpoint_url=self._endpoint_url
            ) as client:
                await client.put_object(
                    Bucket=self._bucket_name,
                    Key=file_name,
                    Body=file_data,
                    ContentType="application/pdf",
                )
                logger.info(
                    f"File {file_name} uploaded to " f"S3 bucket {self._bucket_name}"
                )
        except Exception as e:
            logger.error(f"S3 Upload Error: {e}")
            raise

    async def get_file_url(self, file_name: str) -> str:
        return f"{self._endpoint_url}/{self._bucket_name}/{file_name}"
