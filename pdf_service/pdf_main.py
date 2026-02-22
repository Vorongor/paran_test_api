import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from pdf_service.config.logging_config import setup_logging
from pdf_service.router import pdf_router
from pdf_service.security.exceptions import TokenExpiredError, InvalidTokenError

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    logger.info("PDF Service is starting up...")
    yield


app = FastAPI(title="PDF Service", lifespan=lifespan)

app.include_router(pdf_router)


@app.exception_handler(TokenExpiredError)
async def user_base_exception_handler(
    request: Request, exc: TokenExpiredError  # noqa  # noqa
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content="Token has expired",
    )


@app.exception_handler(InvalidTokenError)
async def user_base_exception_handler(
    request: Request, exc: InvalidTokenError  # noqa  # noqa
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content="Token is invalid",
    )
