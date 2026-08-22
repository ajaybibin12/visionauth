from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.models.user import User


def get_login_token(
    client: TestClient,
    email: str,
) -> str:
    """Login and return the access token."""

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


async def test_get_current_user(
    client: TestClient,
    db_session,
) -> None:
    """Authenticated user should be able to access /auth/me."""

    user = User(
        employee_id="EMP-ME-001",
        email="me@example.com",
        full_name="Current User",
        password_hash=hash_password("StrongPassword123!"),
        is_active=True,
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "me@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user"]["id"] == str(user.id)
    assert data["user"]["email"] == "me@example.com"
    assert data["user"]["full_name"] == "Current User"
    assert "password_hash" not in data["user"]


def test_admin_can_list_users(
    client: TestClient,
    admin_user: User,
) -> None:
    """Admin users should be able to list users."""

    token = get_login_token(
        client,
        admin_user.email,
    )

    response = client.get(
        "/api/v1/users/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert "users" in response.json()


def test_normal_user_cannot_list_users(
    client: TestClient,
    user: User,
) -> None:
    """Normal users should not be able to list users."""

    token = get_login_token(
        client,
        user.email,
    )

    response = client.get(
        "/api/v1/users/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Administrator privileges required."


def test_unauthenticated_user_cannot_list_users(
    client: TestClient,
) -> None:
    """Unauthenticated users should not be able to list users."""

    response = client.get("/api/v1/users/")

    assert response.status_code == 401


def test_admin_can_delete_user(
    client: TestClient,
    admin_user: User,
    user: User,
) -> None:
    """Admin users should be able to delete users."""

    token = get_login_token(
        client,
        admin_user.email,
    )

    response = client.delete(
        f"/api/v1/users/{user.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 204


def test_normal_user_cannot_delete_user(
    client: TestClient,
    user: User,
    admin_user: User,
) -> None:
    """Normal users should not be able to delete users."""

    token = get_login_token(
        client,
        user.email,
    )

    response = client.delete(
        f"/api/v1/users/{admin_user.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_admin_can_update_user(
    client: TestClient,
    admin_user: User,
    user: User,
) -> None:
    """Admin users should be able to update users."""

    token = get_login_token(
        client,
        admin_user.email,
    )

    response = client.patch(
        f"/api/v1/users/{user.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "full_name": "Updated User",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user"]["full_name"] == "Updated User"


def test_normal_user_cannot_update_user(
    client: TestClient,
    user: User,
    admin_user: User,
) -> None:
    """Normal users should not be able to update users."""

    token = get_login_token(
        client,
        user.email,
    )

    response = client.patch(
        f"/api/v1/users/{admin_user.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "full_name": "Hacked Name",
        },
    )

    assert response.status_code == 403
