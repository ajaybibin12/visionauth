from fastapi import Depends, HTTPException, status

from app.db.dependencies import get_current_user
from app.models.enums import UserRole
from app.models.user import User


async def require_admin(
    current_user: User = Depends(get_current_user),  # noqa: B008
) -> User:
    """Require the current user to have administrator privileges."""

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required.",
        )

    return current_user
