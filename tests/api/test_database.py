import pytest
from sqlalchemy import text

from app.db.session import engine


@pytest.mark.asyncio
async def test_database_connection() -> None:
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1
