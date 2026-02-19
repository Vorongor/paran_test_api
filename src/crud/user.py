from datetime import timedelta
from typing import Annotated

from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import BaseAppSettings, get_jwt_manager, get_settings
from src.database import get_db
from src.database.models import UserModel, RefreshTokenModel
from src.exceptions import (
    UserCreateException,
    UserNotFoundException,
    UserAlreadyExistsException,
    PasswordChangeError
)
from src.schemas import (
    UserCreateSchema,
    UserReadSchema,
    LoginRequestSchema,
    LoginResponseSchema
)
from src.security import JWTAuthManagerInterface


async def _get_user_by_email(email: str, db: AsyncSession) -> UserModel:
    user = await db.execute(select(UserModel).where(UserModel.email == email))
    return user.scalar_one_or_none()


async def create_new_user(
        user_data: UserCreateSchema,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> UserReadSchema:
    existing_user = await _get_user_by_email(user_data.email, db)
    if existing_user:
        raise UserAlreadyExistsException(
            message="User with provided email already exists"
        )

    user = UserModel.create(
        email=user_data.email,
        name=user_data.name,
        surname=user_data.surname,
        date_of_birth=user_data.date_of_birth,
        raw_password=user_data.password,
    )
    db.add(user)

    try:
        await db.commit()
        await db.refresh(user)
    except SQLAlchemyError as err:
        await db.rollback()
        raise UserCreateException(
            message=str(err),
        )
    return UserReadSchema.model_validate(user)


async def login_user(
        login_data: LoginRequestSchema,
        db: Annotated[AsyncSession, Depends(get_db)],
        jwt_manager: Annotated[
            JWTAuthManagerInterface, Depends(get_jwt_manager)
        ],
        settings: Annotated[BaseAppSettings, Depends(get_settings)],

) -> LoginResponseSchema:
    user = await _get_user_by_email(login_data.email, db)
    if not user:
        raise UserNotFoundException(
            message="Incorrect email or password"
        )

    if not user.check_password(login_data.password):
        raise PasswordChangeError(
            message="Incorrect email or password"
        )
    token_data = {
        "user_id": user.id,
        "email": user.email,
    }
    access_token = jwt_manager.create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=settings.ACCESS_KEY_TIMEDELTA_MINUTES),
    )
    refresh_token = jwt_manager.create_refresh_token(
        data=token_data,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_DAYS),
    )

    db_token = RefreshTokenModel.create(
        token=refresh_token,
        user_id=user.id,
    )
    db.add(db_token)
    try:
        await db.commit()
        return LoginResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )
    except SQLAlchemyError:
        await db.rollback()
        raise
