"""QR code database model."""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship

from pyshared.models.enums import QRCodeType

from .base import TimestampedModel


class QRCode(TimestampedModel, table=True):
    """QR code model."""

    __tablename__ = "qr_codes"

    id: Optional[str] = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True)
    type: QRCodeType
    target_id: str
    expires_at: Optional[datetime] = None
    is_active: bool = Field(default=True)
    user_id: str = Field(foreign_key="users.id")

    # Relationships
    user: "User" = Relationship(back_populates="qr_codes")