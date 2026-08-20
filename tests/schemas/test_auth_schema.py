from app.schemas.auth import LoginRequest, TokenResponse


def test_login_request_schema() -> None:
    """Test valid login request schema."""

    login_request = LoginRequest(
        email="test@example.com", password="StrongPassword123!"
    )

    assert login_request.email == "test@example.com"
    assert login_request.password == "StrongPassword123!"


def test_token_response_schema() -> None:
    """Test valid token response schema."""

    token_response = TokenResponse(access_token="test-access-token")

    assert token_response.access_token == "test-access-token"
    assert token_response.token_type == "Bearer"
