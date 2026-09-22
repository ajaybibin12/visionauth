from __future__ import annotations

AUTH_URL = "/api/v1/auth"


def login(client) -> dict:
    """Log in the test user and return tokens."""

    response = client.post(
        f"{AUTH_URL}/login",
        json={
            "email": "test@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 200

    return response.json()


def test_change_password_success(
    client,
    user,
) -> None:
    """An authenticated user can change their password."""

    tokens = login(client)

    response = client.post(
        f"{AUTH_URL}/change-password",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
        },
        json={
            "current_password": "StrongPassword123!",
            "new_password": "NewStrongPassword123!",
        },
    )

    assert response.status_code == 204
    assert response.content == b""


def test_change_password_wrong_current_password(
    client,
    user,
) -> None:
    """An incorrect current password is rejected."""

    tokens = login(client)

    response = client.post(
        f"{AUTH_URL}/change-password",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
        },
        json={
            "current_password": "WrongPassword123!",
            "new_password": "NewStrongPassword123!",
        },
    )

    assert response.status_code == 401


def test_change_password_without_authentication(
    client,
    user,
) -> None:
    """Password change requires authentication."""

    response = client.post(
        f"{AUTH_URL}/change-password",
        json={
            "current_password": "StrongPassword123!",
            "new_password": "NewStrongPassword123!",
        },
    )

    assert response.status_code == 401


def test_change_password_invalid_access_token(
    client,
    user,
) -> None:
    """An invalid access token is rejected."""

    response = client.post(
        f"{AUTH_URL}/change-password",
        headers={
            "Authorization": "Bearer invalid-token",
        },
        json={
            "current_password": "StrongPassword123!",
            "new_password": "NewStrongPassword123!",
        },
    )

    assert response.status_code == 401


def test_change_password_missing_current_password(
    client,
    user,
) -> None:
    """Current password is required."""

    tokens = login(client)

    response = client.post(
        f"{AUTH_URL}/change-password",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
        },
        json={
            "new_password": "NewStrongPassword123!",
        },
    )

    assert response.status_code == 422


def test_change_password_missing_new_password(
    client,
    user,
) -> None:
    """New password is required."""

    tokens = login(client)

    response = client.post(
        f"{AUTH_URL}/change-password",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
        },
        json={
            "current_password": "StrongPassword123!",
        },
    )

    assert response.status_code == 422


def test_old_password_no_longer_works(
    client,
    user,
) -> None:
    """The old password cannot be used after changing the password."""

    tokens = login(client)

    response = client.post(
        f"{AUTH_URL}/change-password",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
        },
        json={
            "current_password": "StrongPassword123!",
            "new_password": "NewStrongPassword123!",
        },
    )

    assert response.status_code == 204

    old_login = client.post(
        f"{AUTH_URL}/login",
        json={
            "email": "test@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert old_login.status_code == 401


def test_new_password_can_login(
    client,
    user,
) -> None:
    """The new password can be used to log in."""

    tokens = login(client)

    response = client.post(
        f"{AUTH_URL}/change-password",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
        },
        json={
            "current_password": "StrongPassword123!",
            "new_password": "NewStrongPassword123!",
        },
    )

    assert response.status_code == 204

    new_login = client.post(
        f"{AUTH_URL}/login",
        json={
            "email": "test@example.com",
            "password": "NewStrongPassword123!",
        },
    )

    assert new_login.status_code == 200

    body = new_login.json()

    assert body["access_token"]
    assert body["refresh_token"]
    assert body["token_type"] == "Bearer"
