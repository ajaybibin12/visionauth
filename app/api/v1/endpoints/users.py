from fastapi import APIRouter, Depends, HTTPException, status

from app.db.dependencies import get_user_service
from app.exceptions import (
    EmployeeIDAlreadyExistsError,
    UserAlreadyExistsError,
)
from app.schemas.user import UserCreate, UserRead, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service),  # noqa: B008
) -> UserResponse:
    """Create a new user."""

    try:
        created_user = await user_service.create_user(user_create)
        return UserResponse(user=UserRead.model_validate(created_user))
    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except EmployeeIDAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
