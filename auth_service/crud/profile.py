from typing import Annotated

import httpx
from fastapi import HTTPException, status
from fastapi.params import Depends

from auth_service.config import Settings, get_settings
from auth_service.schemas import UserReadSchema
from auth_service.security.utils import get_current_user


async def generate_pdf_report(
        user: Annotated[UserReadSchema, Depends(get_current_user)],
        settings: Annotated[Settings, Depends(get_settings)]) -> bytes:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=settings.PDF_SERVICE_URL,
                json=user.model_dump(mode="json"),
                timeout=10.0
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="PDF service failed to generate document",
                )
            return response.content
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="PDF service is currently unavailable"
            )