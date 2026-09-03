from __future__ import annotations

from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_session
from app.exceptions import UserNotFoundError
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService

bearer_scheme = HTTPBearer()


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


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),  # noqa: B008
    user_service: UserService = Depends(get_user_service),  # noqa: B008
) -> User:
    """Return the user associated with the access token."""

    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    subject = payload.sub

    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = UUID(subject)
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    try:
        return await user_service.get_user(user_id)
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
