from datetime import datetime, date, timezone, timedelta
from typing import List

from sqlalchemy import Integer, String, DateTime, func, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth_service.config import get_settings
from auth_service.database import Base
from auth_service.security import hash_password, verify_password

settings = get_settings()


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    surname: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    date_of_birth: Mapped[datetime] = mapped_column(Date)
    _hashed_password: Mapped[str] = mapped_column(
        "hashed_password", String(255), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    refresh_tokens: Mapped[List["RefreshTokenModel"]] = relationship(
        "RefreshTokenModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<UserModel(id={self.id}, email={self.email}, "
            f"full name: {self.name} {self.surname})>"
        )

    @classmethod
    def create(
        cls,
        email: str,
        raw_password: str,
        name: str,
        surname: str,
        date_of_birth: date,
    ) -> "UserModel":
        """
        Factory method to create a new UserModel instance.

        This method simplifies the creation of a new user by handling
        password hashing and setting required attributes.
        """
        user = cls(
            email=email,
            name=name,
            surname=surname,
            date_of_birth=date_of_birth,
        )
        user.password = raw_password
        return user

    @property
    def password(self) -> None:
        raise AttributeError(
            "Password is write-only. Use the setter to set the password."
        )

    @password.setter
    def password(self, password: str) -> None:
        hashed_password = hash_password(password)

        self._hashed_password = hashed_password

    def check_password(self, password: str) -> bool:
        return verify_password(password, self._hashed_password)


class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc) + timedelta(days=1),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped[UserModel] = relationship("UserModel", back_populates="refresh_tokens")

    @classmethod
    def create(cls, user_id: int | Mapped[int], token: str) -> "RefreshTokenModel":
        """
        Factory method to create a new RefreshTokenModel instance.
        """
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_DAYS
        )
        return cls(user_id=user_id, expires_at=expires_at, token=token)

    def __repr__(self) -> str:
        return (
            f"<RefreshTokenModel(id={self.id}, "
            f"token={self.token}, expires_at={self.expires_at})>"
        )
