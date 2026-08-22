from enum import StrEnum


class UserRole(StrEnum):
    """Available user roles."""

    USER = "user"
    ADMIN = "admin"
