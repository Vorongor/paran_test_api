from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import BaseAppSettings, get_settings, get_jwt_manager
from src.crud import create_new_user, login_user
from src.database import get_db
from src.exceptions import (
    UserCreateException,
    UserNotFoundException,
    PasswordChangeError
)
from src.schemas import (
    UserReadSchema,
    UserCreateSchema,
    LoginResponseSchema,
    LoginRequestSchema
)
from src.security import JWTAuthManagerInterface

user_router = APIRouter(tags=["Auth"])


@user_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserReadSchema
)
async def register(
        user_data: UserCreateSchema,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> UserReadSchema:
    try:
        return await create_new_user(
            db=db,
            user_data=user_data,
        )
    except UserCreateException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        )


@user_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponseSchema,
)
async def login(
        login_data: LoginRequestSchema,
        db: Annotated[AsyncSession, Depends(get_db)],
        jwt_manager: Annotated[
            JWTAuthManagerInterface, Depends(get_jwt_manager)],
        settings: Annotated[BaseAppSettings, Depends(get_settings)],
) -> LoginResponseSchema:
    try:
        result = await login_user(
            db=db,
            jwt_manager=jwt_manager,
            settings=settings,
            login_data=login_data,
        )
        return result
    except (UserNotFoundException, PasswordChangeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
