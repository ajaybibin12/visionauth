from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import create_access_token
from app.db.dependencies import get_auth_service
from app.exceptions.auth import AuthenticationError
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    login_request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),  # noqa: B008
) -> TokenResponse:
    """Authenticate a user and return an access token."""

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

    access_token = create_access_token(subject=str(user.id))

    return TokenResponse(
        access_token=access_token,
        token_type="Bearer",
    )
