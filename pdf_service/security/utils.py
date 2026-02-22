from typing import Annotated

from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from pdf_service.security.exceptions import (
    TokenExpiredError,
    InvalidTokenError,
)
from pdf_service.security.interfaces import JWTAuthManagerInterface
from pdf_service.config.dependencies import get_jwt_manager

security_scheme = HTTPBearer()


async def get_current_user(
    auth: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
    jwt_manager: Annotated[JWTAuthManagerInterface, Depends(get_jwt_manager)],
) -> None:
    token = auth.credentials
    try:
        jwt_manager.decode_access_token(token)
    except (TokenExpiredError, InvalidTokenError):
        raise
