from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import create_access_token
from app.db.dependencies import (
    get_auth_service,
    get_current_user,
    get_refresh_token_service,
    get_session_service,
)
from app.exceptions.auth import AuthenticationError
from app.models.user import User
from app.schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    LogoutRequest,
    TokenResponse,
)
from app.schemas.user import UserRead, UserResponse
from app.services.auth_service import AuthService
from app.services.refresh_token_service import RefreshTokenService
from app.services.session_service import SessionService

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


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    logout_request: LogoutRequest,
    refresh_token_service: SessionService = Depends(get_session_service),  # noqa: B008
) -> None:
    """Revoke a refresh token."""

    await refresh_token_service.revoke_refresh_token(logout_request.refresh_token)


@router.post(
    "/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def change_password(
    change_password_request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),  # noqa: B008
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
) -> None:
    """Change the password for the currently authenticated user."""

    try:
        await auth_service.change_password(
            user=current_user,
            current_password=change_password_request.current_password,
            new_password=change_password_request.new_password,
        )
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect.",
        ) from exc


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
