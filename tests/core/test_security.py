import jwt

from app.core.config import settings
from app.core.security import (
    create_access_token,
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


def test_create_access_token_contains_subject() -> None:
    """Access token should contain the user subject."""

    token = create_access_token("test-user-123")

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload["sub"] == "test-user-123"
    assert "iat" in payload
    assert "exp" in payload
