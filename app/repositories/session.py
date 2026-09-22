from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import UserSession
from app.repositories.base import BaseRepository


class SessionRepository(BaseRepository[UserSession]):
    """Repository for user session operations."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserSession)

    async def get_by_refresh_token_hash(
        self,
        refresh_token_hash: str,
    ) -> UserSession | None:
        """Return a session by refresh token hash."""

        result = await self.session.execute(
            select(UserSession).where(
                UserSession.refresh_token_hash == refresh_token_hash
            )
        )

        return result.scalar_one_or_none()

    async def revoke(
        self,
        session_id: UUID,
    ) -> None:
        """Revoke a session."""

        await self.session.execute(
            update(UserSession)
            .where(UserSession.id == session_id)
            .values(revoked_at=datetime.now(timezone.utc))
        )

        await self.session.commit()
