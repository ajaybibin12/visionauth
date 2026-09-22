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


def test_logout_success(
    client,
    user,
) -> None:
    """A valid refresh token can be revoked."""

    tokens = login(client)

    response = client.post(
        f"{AUTH_URL}/logout",
        json={
            "refresh_token": tokens["refresh_token"],
        },
    )

    assert response.status_code == 204
    assert response.content == b""


def test_logout_unknown_refresh_token(
    client,
) -> None:
    """An unknown refresh token can be revoked safely."""

    response = client.post(
        f"{AUTH_URL}/logout",
        json={
            "refresh_token": "unknown-refresh-token",
        },
    )

    assert response.status_code == 204


def test_logout_already_revoked_token(
    client,
    user,
) -> None:
    """Logging out twice is safe."""

    tokens = login(client)

    first_response = client.post(
        f"{AUTH_URL}/logout",
        json={
            "refresh_token": tokens["refresh_token"],
        },
    )

    assert first_response.status_code == 204

    second_response = client.post(
        f"{AUTH_URL}/logout",
        json={
            "refresh_token": tokens["refresh_token"],
        },
    )

    assert second_response.status_code == 204


def test_logout_missing_refresh_token(
    client,
) -> None:
    """Refresh token is required."""

    response = client.post(
        f"{AUTH_URL}/logout",
        json={},
    )

    assert response.status_code == 422
