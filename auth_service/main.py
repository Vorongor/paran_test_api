import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from auth_service.config import setup_logging
from auth_service.exceptions import UserBaseException
from auth_service.routers import api_v1_router


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(
        app: FastAPI  # noqa
):
    logger.info("Service is starting up...")
    yield


app = FastAPI(title="Auth Service", lifespan=lifespan)

app.include_router(api_v1_router)


@app.exception_handler(UserBaseException)
async def user_base_exception_handler(
        request: Request,  # noqa
        exc: UserBaseException
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=str(exc),
    )
