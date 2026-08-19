from app.core.security import hash_password, verify_password


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
