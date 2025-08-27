"""Base model for all database models."""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel as PydanticBaseModel, ConfigDict, Field
from sqlmodel import Field as SQLField, SQLModel


class BaseModel(SQLModel):
    """Base model with common fields and configuration."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
        },
    )


class TimestampedModel(BaseModel):
    """Base model with timestamp fields."""

    created_at: datetime = SQLField(default_factory=datetime.utcnow)
    updated_at: datetime = SQLField(default_factory=datetime.utcnow)


class BaseSchema(PydanticBaseModel):
    """Base Pydantic schema with common configuration."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
        },
        from_attributes=True,
    )


class PaginationParams(BaseSchema):
    """Pagination parameters."""

    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(default=20, ge=1, le=100, description="Items per page")


class PaginationResponse(BaseSchema):
    """Pagination response."""

    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool


class ApiResponse(BaseSchema):
    """Standard API response wrapper."""

    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[str] = None
    pagination: Optional[PaginationResponse] = None


class ErrorResponse(BaseSchema):
    """Error response schema."""

    error: str
    message: str
    details: Optional[Dict[str, Any]] = None