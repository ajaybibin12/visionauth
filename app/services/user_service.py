from __future__ import annotations

from uuid import UUID

from app.exceptions import (
    EmployeeIDAlreadyExistsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class UserService:
    """Service layer for user operations."""

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""

        # Check if the email already exists
        existing_user_by_email = await self.user_repository.get_by_email(
            user_create.email
        )

        if existing_user_by_email:
            raise UserAlreadyExistsError(
                f"User with email {user_create.email} already exists."
            )

        # Check if the employee ID already exists
        existing_user_by_employee_id = await self.user_repository.get_by_employee_id(
            user_create.employee_id
        )

        if existing_user_by_employee_id:
            raise EmployeeIDAlreadyExistsError(
                f"User with employee ID {user_create.employee_id} already exists."
            )

        # Create a new user instance
        new_user = User(
            employee_id=user_create.employee_id,
            email=user_create.email,
            full_name=user_create.full_name,
        )

        return await self.user_repository.create(new_user)

    async def get_user(self, user_id: UUID) -> User:
        """Get a user by ID."""

        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(f"User with ID {user_id} not found.")

        return user

    async def get_users(self) -> list[User]:
        """List all users."""

        return await self.user_repository.list()
