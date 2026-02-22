import os
from typing import Annotated

from fastapi import Depends

from auth_service.config import Settings
from auth_service.security import JWTAuthManager


def get_settings() -> Settings:
    """
    Retrieve the application settings based on the current environment.
    """
    return Settings()


def get_jwt_manager(
    settings: Annotated[Settings, Depends(get_settings)],
) -> JWTAuthManager:
    """
    Create and return a JWT authentication manager instance.
    """
    return JWTAuthManager(
        secret_key_access=settings.SECRET_KEY_ACCESS,
        secret_key_refresh=settings.SECRET_KEY_REFRESH,
        algorithm=settings.JWT_SIGNING_ALGORITHM,
    )


SettingsDep = Annotated[Settings, Depends(get_settings)]
JWTManagerDep = Annotated[JWTAuthManager, Depends(get_jwt_manager)]
