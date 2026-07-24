from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema for all models."""

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )


class TimestampedSchema(BaseSchema):
    """Base schema for all models with timestamps."""

    id: UUID
    created_at: datetime
    updated_at: datetime
