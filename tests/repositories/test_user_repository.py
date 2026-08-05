from uuid import uuid4

import pytest

from app.models.user import User
from app.repositories.user import UserRepository


@pytest.mark.asyncio
async def test_create_user(db_session):
    repository = UserRepository(db_session)

    user = User(
        employee_id=f"EMP-{uuid4().hex[:8]}",
        email=f"{uuid4().hex[:8]}@example.com",
        full_name="John Doe",
    )

    created = await repository.create(user)

    assert created.id is not None
    assert created.employee_id == user.employee_id


@pytest.mark.asyncio
async def test_get_by_email(db_session):
    repository = UserRepository(db_session)

    email = f"{uuid4().hex[:8]}@example.com"

    user = User(
        employee_id=f"EMP-{uuid4().hex[:8]}",
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

    user = User(
        employee_id=employee_id,
        email=f"{uuid4().hex[:8]}@example.com",
        full_name="Alex Smith",
    )

    await repository.create(user)

    found = await repository.get_by_employee_id(employee_id)

    assert found is not None
    assert found.employee_id == employee_id
