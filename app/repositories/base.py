from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic repository for CRUD operations."""

    def __init__(
        self,
        session: AsyncSession,
        model: type[ModelType],
    ) -> None:
        self.session = session
        self.model = model

    async def create(self, obj: ModelType) -> ModelType:
        """Create a new database record."""

        self.session.add(obj)
        try:
            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_by_id(self, obj_id: Any) -> ModelType | None:
        """Return an object by primary key."""

        return await self.session.get(self.model, obj_id)

    async def list(
        self, *, offset: int = 0, limit: int | None = None
    ) -> list[ModelType]:
        """Return all records."""

        """Return database records with optional pagination."""

        query = select(self.model)

        if limit is not None:
            query = query.limit(limit)

        query = query.offset(offset)

        result = await self.session.execute(query)

        return list(result.scalars().all())

    async def count(self) -> int:
        """Return the total number of records."""

        result = await self.session.execute(
            select(func.count()).select_from(self.model)
        )

        return result.scalar_one()

    async def delete(self, obj: ModelType) -> None:
        """Delete a database record."""

        await self.session.delete(obj)
        try:
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def update(self) -> None:
        """Commit pending changes."""
        try:
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise
