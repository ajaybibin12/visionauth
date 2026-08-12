import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.db.base import Base
from app.db.session import get_session
from app.main import app

engine = create_async_engine(
    settings.test_database_url,
    future=True,
    poolclass=NullPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_session():
    """Provide a test database session to the application."""

    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Reset database state before and after each test."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())

    yield

    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest_asyncio.fixture
async def db_session():
    """Provide a database session for tests."""

    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
