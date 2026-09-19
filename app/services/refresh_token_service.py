from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.core.config import settings
from app.core.security import generate_refresh_token, hash_refresh_token
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token import RefreshTokenRepository


class RefreshTokenService:
    """Service for refresh token operations."""

    def __init__(
        self,
        refresh_token_repository: RefreshTokenRepository,
    ) -> None:
        self.refresh_token_repository = refresh_token_repository

    async def create_refresh_token(
        self,
        user_id: UUID,
    ) -> str:
        """Create and persist a refresh token."""

        raw_token = generate_refresh_token()

        now = datetime.now(timezone.utc)

        expires_at = now + timedelta(days=settings.jwt_refresh_token_expire_days)

        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=hash_refresh_token(raw_token),
            expires_at=expires_at,
        )

        await self.refresh_token_repository.create(refresh_token)

        return raw_token
