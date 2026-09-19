from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)


def test_hash_password() -> None:
    """Password hashing should return a hash different from the password."""

    password = "StrongPassword123!"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert hashed_password


def test_verify_password_success() -> None:
    """Correct password should successfully verify."""

    password = "StrongPassword123!"

    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_verify_password_failure() -> None:
    """Incorrect password should fail verification."""

    password = "StrongPassword123!"

    hashed_password = hash_password(password)

    assert verify_password("WrongPassword123!", hashed_password) is False


def test_same_password_produces_different_hashes() -> None:
    """Password hashing should use a unique salt."""

    password = "StrongPassword123!"

    hash_one = hash_password(password)
    hash_two = hash_password(password)

    assert hash_one != hash_two

    assert verify_password(password, hash_one) is True
    assert verify_password(password, hash_two) is True


def test_create_access_token() -> None:
    """Access token creation should return a valid JWT."""

    token = create_access_token("test-user-123")

    assert isinstance(token, str)
    assert token.count(".") == 2


def test_create_access_token_contains_expected_claims() -> None:
    """Access token should contain the expected JWT claims."""

    subject = "test-user-123"

    token = create_access_token(subject)

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload["sub"] == subject
    assert payload["type"] == "access"
    assert "iat" in payload
    assert "exp" in payload


def test_decode_access_token() -> None:
    """Valid access token should decode into a validated payload."""

    subject = "test-user-123"

    token = create_access_token(subject)

    payload = decode_access_token(token)

    assert payload.sub == subject
    assert payload.type == "access"
    assert payload.iat is not None
    assert payload.exp is not None


def test_decode_access_token_rejects_invalid_token() -> None:
    """Malformed JWT should be rejected."""

    with pytest.raises(jwt.PyJWTError):
        decode_access_token("invalid-token")


def test_decode_access_token_rejects_wrong_secret() -> None:
    """Token signed with another secret should be rejected."""

    now = datetime.now(timezone.utc)

    payload = {
        "sub": "test-user-123",
        "iat": now,
        "exp": now + timedelta(minutes=30),
        "type": "access",
    }

    token = jwt.encode(
        payload,
        "wrong-secret",
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(jwt.PyJWTError):
        decode_access_token(token)


def test_decode_access_token_rejects_wrong_token_type() -> None:
    """Non-access tokens should be rejected."""

    now = datetime.now(timezone.utc)

    payload = {
        "sub": "test-user-123",
        "iat": now,
        "exp": now + timedelta(minutes=30),
        "type": "refresh",
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(jwt.PyJWTError):
        decode_access_token(token)


def test_decode_access_token_rejects_expired_token() -> None:
    """Expired access tokens should be rejected."""

    now = datetime.now(timezone.utc)

    payload = {
        "sub": "test-user-123",
        "iat": now - timedelta(minutes=60),
        "exp": now - timedelta(minutes=30),
        "type": "access",
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(jwt.PyJWTError):
        decode_access_token(token)


def test_create_refresh_token() -> None:
    """Refresh token should contain the correct claims."""
    user_id = "12345678-1234-1234-1234-123456789012"
    token = create_refresh_token(user_id)
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
    assert payload["sub"] == user_id
    assert payload["type"] == "refresh"
    assert "iat" in payload
    assert "exp" in payload


def test_access_token_cannot_be_used_as_refresh_token() -> None:
    """Access tokens must not be accepted as refresh tokens."""
    token = create_access_token("user-123")
    with pytest.raises(jwt.InvalidTokenError):
        decode_refresh_token(token)


def test_decode_refresh_token() -> None:
    """Valid refresh token should decode successfully."""
    token = create_refresh_token("user-123")
    payload = decode_refresh_token(token)
    assert payload["sub"] == "user-123"
    assert payload["type"] == "refresh"


def test_invalid_access_token() -> None:
    """Invalid access token should be rejected."""
    with pytest.raises(jwt.PyJWTError):
        decode_access_token("invalid-token")


def test_invalid_refresh_token() -> None:
    """Invalid refresh token should be rejected."""
    with pytest.raises(jwt.PyJWTError):
        decode_refresh_token("invalid-token")
