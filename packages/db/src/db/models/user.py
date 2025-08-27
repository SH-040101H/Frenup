"""User database model."""

from datetime import date
from typing import Optional

from sqlmodel import Field, Relationship

from pyshared.models.enums import UserRole, UserStatus

from .base import TimestampedModel


class User(TimestampedModel, table=True):
    """User model."""

    __tablename__ = "users"

    id: Optional[str] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    role: UserRole = Field(default=UserRole.ATHLETE)
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    profile_image_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    height: Optional[float] = Field(default=None, gt=0)  # in cm
    weight: Optional[float] = Field(default=None, gt=0)  # in kg

    # Relationships
    workouts: list["Workout"] = Relationship(back_populates="user")
    assessments: list["Assessment"] = Relationship(back_populates="user")
    file_uploads: list["FileUpload"] = Relationship(back_populates="uploaded_by_user")
    qr_codes: list["QRCode"] = Relationship(back_populates="user")