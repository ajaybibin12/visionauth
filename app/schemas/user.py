from __future__ import annotations

from pydantic import EmailStr, Field

from app.schemas.common import BaseSchema, TimestampedSchema


class UserCreate(BaseSchema):
    """Schema for creating a user."""

    employee_id: str = Field(min_length=1, max_length=50)

    email: EmailStr

    full_name: str = Field(min_length=1, max_length=255)


class UserUpdate(BaseSchema):
    """Schema for updating a user."""

    employee_id: str | None = Field(default=None, min_length=1, max_length=50)

    email: EmailStr | None = None

    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    is_active: bool | None = None


class UserRead(TimestampedSchema):
    """Schema for reading a user."""

    employee_id: str
    email: EmailStr
    full_name: str
    is_active: bool


class UserList(TimestampedSchema):
    """Schema for listing users."""

    user: list[UserRead] = []


class UserResponse(TimestampedSchema):
    """Wrapper schema for user response."""

    user: UserRead
