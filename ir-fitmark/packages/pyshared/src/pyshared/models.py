"""Shared Pydantic models for IR FitMark."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRole(str, Enum):
    """User role enumeration."""
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


class AssessmentType(str, Enum):
    """Fitness assessment type enumeration."""
    PUSHUP = "pushup"
    SITUP = "situp"
    RUNNING = "running"
    FLEXIBILITY = "flexibility"


class AssessmentStatus(str, Enum):
    """Assessment status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ReportPeriod(str, Enum):
    """Report period enumeration."""
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


class BaseModelConfig(BaseModel):
    """Base model with common configuration."""
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        str_strip_whitespace=True,
    )


class UserBase(BaseModelConfig):
    """Base user model."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = UserRole.STUDENT


class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModelConfig):
    """User update model."""
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[UserRole] = None


class User(UserBase):
    """User model."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class FitnessAssessmentBase(BaseModelConfig):
    """Base fitness assessment model."""
    user_id: UUID
    assessment_type: AssessmentType
    score: float = Field(..., ge=0, le=100)
    video_url: Optional[str] = None
    ai_confidence: float = Field(..., ge=0, le=1)
    status: AssessmentStatus = AssessmentStatus.PENDING


class FitnessAssessmentCreate(FitnessAssessmentBase):
    """Fitness assessment creation model."""
    pass


class FitnessAssessmentUpdate(BaseModelConfig):
    """Fitness assessment update model."""
    score: Optional[float] = Field(None, ge=0, le=100)
    video_url: Optional[str] = None
    ai_confidence: Optional[float] = Field(None, ge=0, le=1)
    status: Optional[AssessmentStatus] = None


class FitnessAssessment(FitnessAssessmentBase):
    """Fitness assessment model."""
    id: UUID
    assessed_at: datetime


class ReportBase(BaseModelConfig):
    """Base report model."""
    user_id: UUID
    period: ReportPeriod
    data: Dict[str, Any]
    pdf_url: Optional[str] = None


class ReportCreate(ReportBase):
    """Report creation model."""
    pass


class Report(ReportBase):
    """Report model."""
    id: UUID
    generated_at: datetime


class QRCodeBase(BaseModelConfig):
    """Base QR code model."""
    code: str
    user_id: UUID
    expires_at: datetime
    max_usage: int = Field(default=1, ge=1)
    is_active: bool = True


class QRCodeCreate(QRCodeBase):
    """QR code creation model."""
    pass


class QRCode(QRCodeBase):
    """QR code model."""
    id: UUID
    usage_count: int = 0


class ApiResponse(BaseModelConfig):
    """API response wrapper."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None


class Pagination(BaseModelConfig):
    """Pagination model."""
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
    total: int = Field(default=0, ge=0)
    pages: int = Field(default=0, ge=0)


class PaginatedResponse(BaseModelConfig):
    """Paginated response model."""
    items: List[Any]
    pagination: Pagination


# Token models
class Token(BaseModelConfig):
    """Token model."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModelConfig):
    """Token data model."""
    user_id: Optional[UUID] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None