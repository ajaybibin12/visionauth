import pytest

from app.exceptions import (
    EmployeeIDAlreadyExistsError,
    UserAlreadyExistsError,
)
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
