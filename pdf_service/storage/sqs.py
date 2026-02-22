import json
import aioboto3
import logging

from pdf_service.config.logging_config import setup_logging
from pdf_service.storage.interfaces import SQSStorageInterface

setup_logging()
logger = logging.getLogger(__name__)


class SQSClient(SQSStorageInterface):
    def __init__(
            self,
            endpoint_url: str,
            access_key: str,
            secret_key: str,
            queue_name: str,
            region_name: str
    ):
        self._endpoint_url = endpoint_url
        self._queue_name = queue_name
        self._region_name = region_name
        self._session = aioboto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    async def send_message(self, body: dict) -> None:
        async with self._session.client(
                "sqs",
                endpoint_url=self._endpoint_url,
                region_name=self._region_name
        ) as client:
            result = await client.get_queue_url(QueueName=self._queue_name)

            queue_url = result["QueueUrl"]

            await client.send_message(
                QueueUrl=queue_url, MessageBody=json.dumps(body)
            )
            logger.info(f"Message sent to SQS: {body.get('job_id')}")

    async def receive_messages(self, max_messages: int = 1) -> list[str]:
        async with self._session.client(
                "sqs",
                endpoint_url=self._endpoint_url,
                region_name=self._region_name
        ) as client:
            result = await client.get_queue_url(QueueName=self._queue_name)

            queue_url = result["QueueUrl"]

            response = await client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=10
            )

            return response.get("Messages", [])

    async def delete_message(self, receipt_handle: str):
        async with self._session.client(
                "sqs",
                endpoint_url=self._endpoint_url,
                region_name=self._region_name
        ) as client:
            result = await client.get_queue_url(QueueName=self._queue_name)

            queue_url = result["QueueUrl"]
            await client.delete_message(
                QueueUrl=queue_url, ReceiptHandle=receipt_handle
            )
