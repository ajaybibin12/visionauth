import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User


@pytest.mark.asyncio
async def test_login_success(
    client: TestClient,
    db_session: AsyncSession,
) -> None:
    """Valid credentials should return an access token."""

    password = "StrongPassword123!"

    user = User(
        employee_id="EMP-AUTH-001",
        email="login@example.com",
        full_name="Login User",
        password_hash=hash_password(password),
        is_active=True,
    )

    db_session.add(user)
    await db_session.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": password,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["access_token"]
    assert data["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(
    client: TestClient,
    db_session: AsyncSession,
) -> None:
    """Wrong password should return 401."""

    db_session.add(
        User(
            employee_id="EMP-AUTH-002",
            email="wrong-password@example.com",
            full_name="Wrong Password User",
            password_hash=hash_password("CorrectPassword123!"),
            is_active=True,
        )
    )

    await db_session.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrong-password@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


@pytest.mark.asyncio
async def test_login_unknown_email(
    client: TestClient,
) -> None:
    """Unknown email should return 401."""

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "does-not-exist@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


@pytest.mark.asyncio
async def test_login_inactive_user(
    client: TestClient,
    db_session: AsyncSession,
) -> None:
    """Inactive user should return 401."""

    db_session.add(
        User(
            employee_id="EMP-AUTH-003",
            email="inactive@example.com",
            full_name="Inactive User",
            password_hash=hash_password("StrongPassword123!"),
            is_active=False,
        )
    )

    await db_session.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "inactive@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."
