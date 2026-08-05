import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db.base import Base
from app.main import app

TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:VisionAuth12@localhost:5432/visionauth_test"
)

engine = create_async_engine(
    TEST_DATABASE_URL,
    future=True,
    poolclass=NullPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Create tables before each test and clean them afterwards."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

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
