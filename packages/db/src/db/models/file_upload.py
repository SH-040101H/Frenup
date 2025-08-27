"""File upload database model."""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship

from .base import TimestampedModel


class FileUpload(TimestampedModel, table=True):
    """File upload model."""

    __tablename__ = "file_uploads"

    id: Optional[str] = Field(default=None, primary_key=True)
    filename: str
    original_name: str
    mime_type: str
    size: int = Field(gt=0)
    url: str
    uploaded_by: str = Field(foreign_key="users.id")

    # Relationships
    uploaded_by_user: "User" = Relationship(back_populates="file_uploads")