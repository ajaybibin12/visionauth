from datetime import datetime

from pydantic import BaseModel


class AccessTokenPayload(BaseModel):
    """JWT access token payload."""

    sub: str
    iat: datetime
    exp: datetime
    type: str
