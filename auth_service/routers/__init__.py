from auth_service.routers.user import user_router
from auth_service.routers.profile import profile_router
from auth_service.routers.api import api_v1_router

__all__ = ["user_router", "profile_router", "api_v1_router"]
