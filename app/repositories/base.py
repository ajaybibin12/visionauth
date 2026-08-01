from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import select
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
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self, obj_id: Any) -> ModelType | None:
        """Return an object by primary key."""

        return await self.session.get(self.model, obj_id)

    async def list(self) -> list[ModelType]:
        """Return all records."""

        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def delete(self, obj: ModelType) -> None:
        """Delete a database record."""

        await self.session.delete(obj)
        await self.session.commit()

    async def update(self) -> None:
        """Commit pending changes."""

        await self.session.commit()
