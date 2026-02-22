from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, status, HTTPException, Response

from auth_service.config import Settings, get_settings
from auth_service.exceptions import UserBaseException
from auth_service.schemas import UserReadSchema
from auth_service.security.utils import get_current_user

profile_router = APIRouter(tags=["Profile"])


@profile_router.get(
    "/me/profile",
    summary="Download user profile PDF",
    description="Return a PDF document containing user profile details.",
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "A PDF file representing the user profile.",
        },
        401: {"description": "Invalid or expired token"},
    },
)
async def get_profile(
    auth_user: Annotated[UserReadSchema, Depends(get_current_user)],
        settings: Annotated[Settings, Depends(get_settings)]
) -> Response:
    """
    Endpoint to retrieve the current user's profile in PDF format.

    - **Authentication**: Required via Bearer Token
    - **Returns**: Binary PDF stream
    """

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                settings.PDF_SERVICE_URL, json=auth_user.model_dump(mode="json")
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="PDF service error",
                )

            return Response(
                content=response.content,
                media_type="application/pdf",
                headers={
                    "Content-Disposition":
                        f'attachment; filename="profile_{auth_user.id}.pdf"'
                },
            )
        except UserBaseException as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=str(err)
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=503, detail="PDF service unavailable"
            )
