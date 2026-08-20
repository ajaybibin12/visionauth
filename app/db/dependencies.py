from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.user import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService


async def get_user_service(
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> UserService:
    """Return a user service instance."""

    repository = UserRepository(session)

    return UserService(repository)


async def get_auth_service(
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> AuthService:
    """Return an authentication service instance."""

    return AuthService(session)
