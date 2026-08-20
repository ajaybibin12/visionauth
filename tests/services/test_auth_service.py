from uuid import uuid4

import pytest

from app.core.security import hash_password
from app.exceptions.auth import AuthenticationError
from app.models.user import User
from app.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_authenticate_user_success(db_session) -> None:
    """Active user with correct credentials should authenticate successfully."""

    password = "StrongPassword123!"

    user = User(
        id=uuid4(),
        employee_id="EMP-AUTH-001",
        email="auth@example.com",
        full_name="Auth User",
        password_hash=hash_password(password),
        is_active=True,
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    auth_service = AuthService(db_session)

    authenticated_user = await auth_service.authenticate_user(
        email="auth@example.com",
        password=password,
    )

    assert authenticated_user.id == user.id
    assert authenticated_user.email == "auth@example.com"


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(db_session) -> None:
    """Incorrect password should raise AuthenticationError."""

    user = User(
        id=uuid4(),
        employee_id="EMP-AUTH-002",
        email="wrong-password@example.com",
        full_name="Wrong Password User",
        password_hash=hash_password("CorrectPassword123!"),
        is_active=True,
    )

    db_session.add(user)
    await db_session.commit()

    auth_service = AuthService(db_session)

    with pytest.raises(
        AuthenticationError,
        match="Invalid email or password",
    ):
        await auth_service.authenticate_user(
            email="wrong-password@example.com",
            password="WrongPassword123!",
        )


@pytest.mark.asyncio
async def test_authenticate_user_unknown_email(db_session) -> None:
    """Unknown email should raise AuthenticationError."""

    auth_service = AuthService(db_session)

    with pytest.raises(
        AuthenticationError,
        match="Invalid email or password",
    ):
        await auth_service.authenticate_user(
            email="does-not-exist@example.com",
            password="StrongPassword123!",
        )


@pytest.mark.asyncio
async def test_authenticate_inactive_user(db_session) -> None:
    """Inactive user should not be allowed to authenticate."""

    user = User(
        id=uuid4(),
        employee_id="EMP-AUTH-003",
        email="inactive@example.com",
        full_name="Inactive User",
        password_hash=hash_password("StrongPassword123!"),
        is_active=False,
    )

    db_session.add(user)
    await db_session.commit()

    auth_service = AuthService(db_session)

    with pytest.raises(
        AuthenticationError,
        match="Invalid email or password",
    ):
        await auth_service.authenticate_user(
            email="inactive@example.com",
            password="StrongPassword123!",
        )
