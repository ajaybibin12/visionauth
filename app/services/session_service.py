from __future__ import annotations

from app.core.security import hash_refresh_token
from app.repositories.session import SessionRepository


class SessionService:
    """Service layer for authenticated sessions."""

    def __init__(self, session_repository: SessionRepository) -> None:
        self.session_repository = session_repository

    async def revoke_refresh_token(
        self,
        refresh_token: str,
    ) -> None:
        """Revoke a refresh token."""

        token_hash = hash_refresh_token(refresh_token)

        user_session = await self.session_repository.get_by_refresh_token_hash(
            token_hash
        )

        if user_session is None:
            return

        await self.session_repository.revoke(user_session.id)
