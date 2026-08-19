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
from app.db.session import get_session
from app.main import app
from app.models.user import User
from app.repositories.user import UserRepository

engine = create_async_engine(
    settings.test_database_url,
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

    async with TestingSessionLocal() as session:
        for table in reversed(User.metadata.sorted_tables):
            await session.execute(table.delete())

        await session.commit()

    yield

    async with TestingSessionLocal() as session:
        for table in reversed(User.metadata.sorted_tables):
            await session.execute(table.delete())

        await session.commit()


@pytest_asyncio.fixture
async def db_session():
    """Provide a database session for tests."""

    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def user_repository(
    db_session: AsyncSession,
) -> UserRepository:
    """Provide a user repository for service tests."""

    return UserRepository(db_session)


@pytest_asyncio.fixture
async def user(db_session: AsyncSession) -> User:
    """Create and return a test user."""

    test_user = User(
        employee_id="EMP001",
        email="test@example.com",
        full_name="Test User",
        password_hash="test-password-hash",
        is_active=True,
    )

    db_session.add(test_user)
    await db_session.commit()
    await db_session.refresh(test_user)

    return test_user


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
