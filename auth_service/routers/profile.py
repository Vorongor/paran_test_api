from typing import Annotated

import httpx
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    Response,
    Request
)
from fastapi.responses import JSONResponse

from auth_service.config import Settings, get_settings
from auth_service.crud.profile import generate_pdf_report
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
        request: Request,
        user: Annotated[UserReadSchema, Depends(get_current_user)],
        settings: Annotated[Settings, Depends(get_settings)]
) -> Response:
    """
    Endpoint to retrieve the current user's profile in PDF format.

    - **Authentication**: Required via Bearer Token
    - **Returns**: Binary PDF stream
    """

    try:
        response = await generate_pdf_report(
            request=request,
            user=user,
            url=settings.PDF_SERVICE_URL,

        )
        return Response(
            content=response.content,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                    f'attachment; filename="profile_{user.id}.pdf"'
            },
        )
    except UserBaseException as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(err)
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="PDF service is currently unavailable"
        )

@profile_router.get(
    "/me/profile-in-storage",
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
async def get_profile_in_storage(
        request: Request,
        user: Annotated[UserReadSchema, Depends(get_current_user)],
        settings: Annotated[Settings, Depends(get_settings)]
) -> Response:
    """
    Endpoint to generate the current user's profile in PDF format and save it
    in storage. Return a link to file in storage.

    - **Authentication**: Required via Bearer Token
    - **Returns**: Response with link inside
    """

    try:
        response = await generate_pdf_report(
            request=request,
            user=user,
            url=settings.PDF_SERVICE_URL_IN_STORAGE,

        )
        return JSONResponse(
        content=response.json(),
        status_code=response.status_code
    )
    except UserBaseException as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(err)
        )
    except httpx.RequestError as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            # detail="PDF service is currently unavailable"
            detail=str(err),
        )
