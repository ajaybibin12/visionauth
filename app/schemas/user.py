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
