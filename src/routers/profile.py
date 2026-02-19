from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Response

from src.crud import prepare_profile_pdf_response
from src.exceptions import (
    TokenExpiredError,
    InvalidTokenError,
    UserNotFoundException,
)
from src.schemas import UserReadSchema
from src.security.utils import get_current_user

profile_router = APIRouter(tags=["Profile"])


@profile_router.get(
    "/profile",
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
) -> Response:
    """
    Endpoint to retrieve the current user's profile in PDF format.

    - **Authentication**: Required via Bearer Token
    - **Returns**: Binary PDF stream
    """
    try:
        return await prepare_profile_pdf_response(auth_user)

    except (TokenExpiredError, InvalidTokenError) as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=getattr(err, "message", "Authentication failed"),
        )
    except UserNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=err.message
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating the PDF report.",
        )
