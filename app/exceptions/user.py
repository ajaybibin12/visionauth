class UserError(Exception):
    """Base exception for user errors."""


class UserAlreadyExistsError(UserError):
    """Raised when a user with the same email already exists."""


class EmployeeIDAlreadyExistsError(UserError):
    """Raised when an employee ID already exists."""


class UserNotFoundError(UserError):
    """Raised when a user cannot be found."""
