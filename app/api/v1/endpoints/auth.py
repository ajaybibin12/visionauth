from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import create_access_token
from app.db.dependencies import (
    get_auth_service,
    get_current_user,
    get_refresh_token_service,
)
from app.exceptions.auth import AuthenticationError
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserRead, UserResponse
from app.services.auth_service import AuthService
from app.services.refresh_token_service import RefreshTokenService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    login_request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
    refresh_token_service: RefreshTokenService = Depends(  # noqa: B008
        get_refresh_token_service
    ),
) -> TokenResponse:
    """Authenticate a user and return access and refresh tokens."""

    try:
        user = await auth_service.authenticate_user(
            email=login_request.email,
            password=login_request.password,
        )
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        ) from exc

    access_token = create_access_token(
        subject=str(user.id),
    )

    refresh_token = await refresh_token_service.create_refresh_token(
        user_id=user.id,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),  # noqa: B008
) -> UserResponse:
    """Return the currently authenticated user's profile."""

    return UserResponse(
        user=UserRead.model_validate(current_user),
    )
