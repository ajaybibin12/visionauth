from __future__ import annotations

from app.exceptions import (
    EmployeeIDAlreadyExistsError,
    UserAlreadyExistsError,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class UserService:
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
