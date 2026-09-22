from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.exceptions.auth import AuthenticationError
from app.models.user import User
from app.repositories.user import UserRepository


class AuthService:
    """Service layer for authentication operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repository = UserRepository(session)

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> User:
        """Authenticate a user using email and password."""

        user = await self.user_repository.get_by_email(email)

        if user is None:
            raise AuthenticationError("Invalid email or password.")

        if not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationError("Invalid email or password.")

        return user

    async def change_password(
        self,
        user: User,
        current_password: str,
        new_password: str,
    ) -> None:
        """Change the password for the authenticated user."""

        if not verify_password(
            current_password,
            user.password_hash,
        ):
            raise AuthenticationError("Current password is incorrect.")

        user.password_hash = hash_password(new_password)

        await self.session.commit()
