"""Base database models."""

from datetime import datetime
from typing import Any

from sqlmodel import Field, SQLModel
from pydantic import ConfigDict


class BaseModel(SQLModel):
    """Base model with common configuration."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
        },
    )


class TimestampedModel(BaseModel):
    """Base model with timestamp fields."""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)