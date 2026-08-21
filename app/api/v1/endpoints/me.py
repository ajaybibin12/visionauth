from fastapi import APIRouter, Depends

from app.db.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserRead, UserResponse

router = APIRouter(prefix="/me", tags=["Authentication"])


@router.get("", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),  # noqa: B008
) -> UserResponse:
    """Return the currently authenticated user's profile."""

    return UserResponse(user=UserRead.model_validate(current_user))
