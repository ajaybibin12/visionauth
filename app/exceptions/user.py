class UserAlreadyExistsError(Exception):
    """Raised when a user already exists."""


class EmployeeIDAlreadyExistsError(Exception):
    """Raised when an employee ID already exists."""


class UserNotFoundError(Exception):
    """Raised when a user cannot be found."""


class UserError(Exception):
    """Base exception for all user-related errors."""
