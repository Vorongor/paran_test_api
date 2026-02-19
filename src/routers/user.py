from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import JWTManagerDep, SettingsDep
from src.crud import create_new_user, login_user
from src.database import get_db
from src.exceptions import UserBaseException, BaseSecurityException
from src.schemas import (
    UserReadSchema,
    UserCreateSchema,
    LoginResponseSchema,
    LoginRequestSchema,
)

user_router = APIRouter(tags=["Authentication"])


@user_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserReadSchema,
    summary="Register a new user",
    responses={
        400: {"description": "User already exists or validation error"},
        422: {"description": "Validation Error"},
    },
)
async def register(
    user_data: UserCreateSchema, db: Annotated[AsyncSession, Depends(get_db)]
) -> UserReadSchema:
    """
    Register a new user in the system.

    - **email**: Must be unique
    - **password**: Should be strong (minimum 8 characters,
    1 uppercase letter, 1 digit, 1 special character)
    - **name/surname**: User's personal details
    """
    try:
        return await create_new_user(
            db=db,
            user_data=user_data,
        )
    except UserBaseException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        )


@user_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponseSchema,
    summary="Authenticate user and get tokens",
    responses={
        400: {"description": "Invalid credentials"},
        401: {"description": "Unauthorized"},
    },
)
async def login(
    login_data: LoginRequestSchema,
    db: Annotated[AsyncSession, Depends(get_db)],
    jwt_manager: JWTManagerDep,
    settings: SettingsDep,
) -> LoginResponseSchema:
    """
    Authenticate a user and return JWT tokens.

    - **email**: Registered user email
    - **password**: Valid password
    - **Returns**: Access and Refresh tokens
    """
    try:
        result = await login_user(
            db=db,
            jwt_manager=jwt_manager,
            settings=settings,
            login_data=login_data,
        )
        return result
    except (UserBaseException, BaseSecurityException):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
