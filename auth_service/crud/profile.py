import logging
from typing import Annotated

import httpx

from fastapi import HTTPException, status, Request, Response
from fastapi.params import Depends

from auth_service.config import setup_logging
from auth_service.schemas import UserReadSchema
from auth_service.security.utils import get_current_user

setup_logging()
logger = logging.getLogger(__name__)


async def generate_pdf_report(
    request: Request,
    user: Annotated[UserReadSchema, Depends(get_current_user)],
    url: str,
) -> Response:
    auth_header = request.headers.get("Authorization")

    logger.info(f"Generating PDF report for {url}")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=url,
            json=user.model_dump(mode="json"),
            headers={"Authorization": auth_header},
            timeout=10.0,
        )
        return response
