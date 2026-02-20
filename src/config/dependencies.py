import os
from typing import Annotated

from fastapi import Depends

from src.config import (
    Settings,
    BaseAppSettings,
    TestingSettings,
    LocalSettings,
)
from src.security import JWTAuthManager


def get_settings() -> BaseAppSettings:
    """
    Retrieve the application settings based on the current environment.
    """

    env = os.getenv("ENVIRONMENT", "local").lower()

    configs = {
        "docker": Settings,
        "test": TestingSettings,
        "local": LocalSettings,
    }

    config_class = configs.get(env, LocalSettings)
    return config_class()


def get_jwt_manager(
    settings: Annotated[BaseAppSettings, Depends(get_settings)],
) -> JWTAuthManager:
    """
    Create and return a JWT authentication manager instance.
    """
    return JWTAuthManager(
        secret_key_access=settings.SECRET_KEY_ACCESS,
        secret_key_refresh=settings.SECRET_KEY_REFRESH,
        algorithm=settings.JWT_SIGNING_ALGORITHM,
    )


SettingsDep = Annotated[BaseAppSettings, Depends(get_settings)]
JWTManagerDep = Annotated[JWTAuthManager, Depends(get_jwt_manager)]
