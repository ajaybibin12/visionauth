from uuid import uuid4

import pytest

from app.models.user import User
from app.repositories.user import UserRepository


def make_user(
    *,
    employee_id: str | None = None,
    email: str | None = None,
    full_name: str = "John Doe",
) -> User:
    return User(
        employee_id=employee_id or f"EMP-{uuid4().hex[:8]}",
        email=email or f"{uuid4().hex[:8]}@example.com",
        full_name=full_name,
        password_hash="test-password-hash",
        is_active=True,
    )


@pytest.mark.asyncio
async def test_create_user(db_session):
    repository = UserRepository(db_session)

    user = make_user()

    created = await repository.create(user)

    assert created.id is not None
    assert created.employee_id == user.employee_id


@pytest.mark.asyncio
async def test_get_by_email(db_session):
    repository = UserRepository(db_session)

    email = f"{uuid4().hex[:8]}@example.com"

    user = make_user(
        email=email,
        full_name="Jane Doe",
    )

    await repository.create(user)

    found = await repository.get_by_email(email)

    assert found is not None
    assert found.email == email


@pytest.mark.asyncio
async def test_get_by_employee_id(db_session):
    repository = UserRepository(db_session)

    employee_id = f"EMP-{uuid4().hex[:8]}"

    user = make_user(
        employee_id=employee_id,
        full_name="Alex Smith",
    )

    await repository.create(user)

    found = await repository.get_by_employee_id(employee_id)

    assert found is not None
    assert found.employee_id == employee_id


@pytest.mark.asyncio
async def test_list_users(db_session):
    """Repository should return all users."""

    user_1 = make_user(
        employee_id="EMP-001",
        email="john@example.com",
        full_name="John Doe",
    )

    user_2 = make_user(
        employee_id="EMP-002",
        email="jane@example.com",
        full_name="Jane Doe",
    )

    db_session.add_all([user_1, user_2])
    await db_session.commit()

    repository = UserRepository(db_session)

    users = await repository.list()

    assert len(users) == 2
    assert users[0].employee_id == "EMP-001"
    assert users[1].employee_id == "EMP-002"
