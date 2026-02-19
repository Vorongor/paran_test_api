from fastapi import APIRouter

from src.config import get_settings
from src.routers import user_router, profile_router

settings = get_settings()

api_v1_router = APIRouter(prefix=settings.API_V1_PREFIX)

api_v1_router.include_router(user_router)
api_v1_router.include_router(profile_router)
