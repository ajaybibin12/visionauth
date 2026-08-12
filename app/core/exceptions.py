from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import (
    EmployeeIDAlreadyExistsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers."""

    @app.exception_handler(UserAlreadyExistsError)
    async def user_exists_handler(
        request: Request,
        exc: UserAlreadyExistsError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(EmployeeIDAlreadyExistsError)
    async def employee_exists_handler(
        request: Request,
        exc: EmployeeIDAlreadyExistsError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(UserNotFoundError)
    async def user_not_found_handler(
        request: Request,
        exc: UserNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )
