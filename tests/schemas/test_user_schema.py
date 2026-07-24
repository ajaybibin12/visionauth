from app.schemas.user import UserCreate


def test_create_user_schema() -> None:
    """Test user creation schema."""

    user = UserCreate(
        employee_id="EMP001",
        email="john@example.com",
        full_name="John Doe",
    )

    assert user.employee_id == "EMP001"
    assert user.email == "john@example.com"
    assert user.full_name == "John Doe"
