from __future__ import annotations

import re

from pydantic import EmailStr, Field, field_validator

from app.models.enums import UserRole
from app.schemas.common import BaseSchema, TimestampedSchema


class UserCreate(BaseSchema):
    """Schema for creating a user."""

    employee_id: str = Field(min_length=1, max_length=50)

    email: EmailStr

    full_name: str = Field(min_length=1, max_length=255)

    password: str = Field(
        min_length=12,
        max_length=128,
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        """Validate password strength."""

        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")

        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter.")

        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number.")

        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValueError("Password must contain at least one special character.")

        return password


class UserUpdate(BaseSchema):
    """Schema for updating a user."""

    employee_id: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    email: EmailStr | None = None

    full_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    is_active: bool | None = None


class UserRead(TimestampedSchema):
    """Schema for reading a user."""

    employee_id: str
    email: EmailStr
    full_name: str
    is_active: bool
    role: UserRole


class UserList(BaseSchema):
    """Schema for listing users."""

    users: list[UserRead] = Field(default_factory=list)
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total_pages: int = Field(ge=0)


class UserResponse(BaseSchema):
    """Wrapper schema for user response."""

    user: UserRead
