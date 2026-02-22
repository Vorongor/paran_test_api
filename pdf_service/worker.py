import asyncio
import json
import logging

from pdf_service.config.logging_config import setup_logging
from pdf_service.schemas import UserReadSchema
from pdf_service.services import generate_user_pdf
from pdf_service.config import get_settings
from pdf_service.config.dependencies import get_s3_manager, get_sqs_manager

setup_logging()
logger = logging.getLogger(__name__)


async def run_worker():
    settings = get_settings()
    s3 = await get_s3_manager(settings)
    sqs = await get_sqs_manager(settings)

    logger.info("PDF Worker started. Waiting for messages...")

    while True:
        try:
            messages = await sqs.receive_messages(max_messages=1)

            for msg in messages:
                body = json.loads(msg["Body"])
                job_id = body.get("job_id")
                user_data = body.get("user_data")

                logger.info(f"Processing job: {job_id}")

                pdf_bytes = generate_user_pdf(UserReadSchema(
                    id=user_data.get("id"),
                    name=user_data.get("name"),
                    surname=user_data.get("surname"),
                    email=user_data.get("email"),
                    date_of_birth=user_data.get("date_of_birth"),
                ))

                file_name = f"{job_id}.pdf"
                await s3.upload_file(file_name, pdf_bytes)

                await sqs.delete_message(msg["ReceiptHandle"])
                logger.info(f"Job {job_id} completed successfully.")

        except Exception as error:
            logger.error(f"Worker error: {error}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(run_worker())
