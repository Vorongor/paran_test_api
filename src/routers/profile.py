from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Response

from src.exceptions import (
    TokenExpiredError,
    InvalidTokenError,
    UserNotFoundException
)
from src.schemas import UserReadSchema
from src.security.utils import get_current_user
from src.services import generate_user_pdf

profile_router = APIRouter(tags=["Profile"])


@profile_router.get("/profile")
async def get_profile(
        auth_user: Annotated[UserReadSchema, Depends(get_current_user)]
) -> Response:
    try:
        pdf_file = generate_user_pdf(auth_user)

        headers = {
            "Content-Disposition":
                f'attachment; filename="profile_{auth_user.id}.pdf"'
        }

        return Response(
            content=pdf_file.getvalue(),
            media_type="application/pdf",
            headers=headers
        )
    except (
            TokenExpiredError,
            InvalidTokenError,
            UserNotFoundException
    ) as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err.detail,
        )
