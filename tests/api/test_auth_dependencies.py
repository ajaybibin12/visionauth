from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_auth_service
from app.services.auth_service import AuthService


async def test_get_auth_service(db_session: AsyncSession) -> None:
    """Test that the auth dependency returns an AuthService."""

    auth_service = await get_auth_service(db_session)

    assert isinstance(auth_service, AuthService)
    assert auth_service.session is db_session
