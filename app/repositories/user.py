from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for user database operations."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        """Return a user by email."""

        result = await self.session.execute(select(User).where(User.email == email))

        return result.scalar_one_or_none()

    async def get_by_employee_id(
        self,
        employee_id: str,
    ) -> User | None:
        """Return a user by employee ID."""

        result = await self.session.execute(
            select(User).where(User.employee_id == employee_id)
        )

        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int | None = None,
    ) -> list[User]:
        """Return users with pagination."""

        query = select(User).order_by(User.created_at)

        if limit is not None:
            query = query.limit(limit)

        query = query.offset(offset)

        result = await self.session.execute(query)

        return list(result.scalars().all())
