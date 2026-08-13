from uuid import uuid4

import pytest

from app.exceptions import (
    EmployeeIDAlreadyExistsError,
    UserAlreadyExistsError,
)
from app.exceptions.user import UserNotFoundError
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.services.user_service import UserService


@pytest.mark.asyncio
async def test_create_user(db_session):
    """Service should create a user."""

    repository = UserRepository(db_session)
    service = UserService(repository)

    user = await service.create_user(
        UserCreate(
            employee_id="EMP-001",
            email="john@example.com",
            full_name="John Doe",
        )
    )

    assert user.email == "john@example.com"
    assert user.employee_id == "EMP-001"
    assert user.full_name == "John Doe"
    assert user.is_active is True


@pytest.mark.asyncio
async def test_create_user_duplicate_email(db_session):
    """Creating a user with an existing email should fail."""

    repository = UserRepository(db_session)
    service = UserService(repository)

    await service.create_user(
        UserCreate(
            employee_id="EMP-001",
            email="john@example.com",
            full_name="John Doe",
        )
    )

    with pytest.raises(UserAlreadyExistsError):
        await service.create_user(
            UserCreate(
                employee_id="EMP-002",
                email="john@example.com",
                full_name="Jane Doe",
            )
        )


@pytest.mark.asyncio
async def test_create_user_duplicate_employee_id(db_session):
    """Creating a user with an existing employee ID should fail."""

    repository = UserRepository(db_session)
    service = UserService(repository)

    await service.create_user(
        UserCreate(
            employee_id="EMP-001",
            email="john@example.com",
            full_name="John Doe",
        )
    )

    with pytest.raises(EmployeeIDAlreadyExistsError):
        await service.create_user(
            UserCreate(
                employee_id="EMP-001",
                email="jane@example.com",
                full_name="Jane Doe",
            )
        )


@pytest.mark.asyncio
async def test_get_user(user_repository, user):
    """User service should return a user by ID."""

    service = UserService(user_repository)

    result = await service.get_user(user.id)

    assert result.id == user.id
    assert result.email == user.email
    assert result.employee_id == user.employee_id


@pytest.mark.asyncio
async def test_get_user_not_found(user_repository):
    """User service should raise UserNotFoundError if user does not exist."""

    service = UserService(user_repository)
    user_id = uuid4()

    with pytest.raises(UserNotFoundError):
        await service.get_user(user_id)


async def test_get_users(db_session):
    """Service should return all users."""

    user_1 = User(
        employee_id="EMP-001",
        email="john@example.com",
        full_name="John Doe",
    )

    user_2 = User(
        employee_id="EMP-002",
        email="jane@example.com",
        full_name="Jane Doe",
    )

    db_session.add_all([user_1, user_2])
    await db_session.commit()

    repository = UserRepository(db_session)
    service = UserService(repository)

    users = await service.get_users()

    assert len(users) == 2
    assert users[0].employee_id == "EMP-001"
    assert users[1].employee_id == "EMP-002"
