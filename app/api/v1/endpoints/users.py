from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.db.dependencies import get_user_service
from app.exceptions import (
    EmployeeIDAlreadyExistsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.schemas.user import UserCreate, UserList, UserRead, UserResponse, UserUpdate
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
    except EmployeeIDAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),  # noqa: B008
) -> UserResponse:
    """Get a user by ID."""

    try:
        user = await user_service.get_user(user_id)
        return UserResponse(user=UserRead.model_validate(user))
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get("/", response_model=UserList)
async def list_users(
    user_service: UserService = Depends(get_user_service),  # noqa: B008
) -> UserList:
    """List all users."""

    users = await user_service.get_users()
    return UserList(users=[UserRead.model_validate(user) for user in users])


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    user_service: UserService = Depends(get_user_service),  # noqa: B008
) -> UserResponse:
    """Update a user by ID."""

    try:
        updated_user = await user_service.update_user(
            user_id,
            user_update,
        )

        return UserResponse(user=UserRead.model_validate(updated_user))

    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    except EmployeeIDAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
