import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from pdf_service.config.logging_config import setup_logging
from pdf_service.router import pdf_router


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(
        app: FastAPI  # noqa
):
    logger.info("PDF Service is starting up...")
    yield


app = FastAPI(title="PDF Service", lifespan=lifespan)

app.include_router(pdf_router)
