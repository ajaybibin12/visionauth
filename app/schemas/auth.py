from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Schema for login request."""

    email: EmailStr
    password: str


class LogoutRequest(BaseModel):
    """Schema for logout request."""

    refresh_token: str


class ChangePasswordRequest(BaseModel):
    """Schema for changing a password."""

    current_password: str
    new_password: str


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
