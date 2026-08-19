import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate


def test_create_user_schema() -> None:
    """Test valid user creation schema."""

    user = UserCreate(
        employee_id="EMP001",
        email="john@example.com",
        full_name="John Doe",
        password="SecurePassword123!",
    )

    assert user.employee_id == "EMP001"
    assert user.email == "john@example.com"
    assert user.full_name == "John Doe"
    assert user.password == "SecurePassword123!"


def test_create_user_requires_password() -> None:
    """Password is required when creating a user."""

    with pytest.raises(ValidationError):
        UserCreate(
            employee_id="EMP001",
            email="john@example.com",
            full_name="John Doe",
        )


def test_create_user_rejects_short_password() -> None:
    """Password shorter than 12 characters should be rejected."""

    with pytest.raises(ValidationError):
        UserCreate(
            employee_id="EMP001",
            email="john@example.com",
            full_name="John Doe",
            password="Pass123!",
        )


def test_create_user_accepts_valid_password() -> None:
    """Password with at least 12 characters and a special character is accepted."""

    user = UserCreate(
        employee_id="EMP001",
        email="john@example.com",
        full_name="John Doe",
        password="Password123!",
    )

    assert user.password == "Password123!"


def test_create_user_rejects_invalid_email() -> None:
    """Invalid email should be rejected."""

    with pytest.raises(ValidationError):
        UserCreate(
            employee_id="EMP001",
            email="invalid-email",
            full_name="John Doe",
            password="Password123!",
        )


def test_create_user_rejects_empty_full_name() -> None:
    """Empty full name should be rejected."""

    with pytest.raises(ValidationError):
        UserCreate(
            employee_id="EMP001",
            email="john@example.com",
            full_name="",
            password="Password123!",
        )


def test_create_user_rejects_empty_employee_id() -> None:
    """Empty employee ID should be rejected."""

    with pytest.raises(ValidationError):
        UserCreate(
            employee_id="",
            email="john@example.com",
            full_name="John Doe",
            password="Password123!",
        )
