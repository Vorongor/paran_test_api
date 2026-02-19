from typing import Annotated

from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.database.models import UserModel
from src.exceptions import (
    TokenExpiredError,
    InvalidTokenError,
    UserNotFoundException,
)
from src.schemas import UserReadSchema
from src.security import JWTAuthManagerInterface
from src.config import get_jwt_manager

security_scheme = HTTPBearer()


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
    jwt_manager: Annotated[JWTAuthManagerInterface, Depends(get_jwt_manager)],
) -> UserReadSchema:
    token = auth.credentials
    try:
        user_data = jwt_manager.decode_access_token(token)

    except (TokenExpiredError, InvalidTokenError):
        raise

    user_id = user_data.get("user_id")

    auth_user = await db.get(UserModel, user_id)

    if not auth_user:
        raise UserNotFoundException(
            message="User not found with provided credentials.",
        )

    return UserReadSchema.model_validate(auth_user)
