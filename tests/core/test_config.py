from app.core.config import settings


def test_jwt_configuration() -> None:
    """JWT configuration should be available."""

    assert settings.jwt_secret_key
    assert settings.jwt_algorithm == "HS256"
    assert settings.jwt_access_token_expire_minutes == 30
