from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken
from app.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """Repository for refresh token operations."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RefreshToken)

    async def get_by_token_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        """Return a refresh token by its hash."""

        result = await self.session.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash,
            )
        )

        return result.scalar_one_or_none()

    async def revoke(
        self,
        refresh_token: RefreshToken,
        revoked_at: datetime,
    ) -> None:
        """Revoke a refresh token."""

        refresh_token.revoked_at = revoked_at

        await self.session.commit()

        await self.session.refresh(refresh_token)
