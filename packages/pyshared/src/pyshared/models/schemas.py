"""Pydantic schemas for API requests and responses."""

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, EmailStr

from .base import BaseSchema, PaginationParams
from .enums import (
    AssessmentStatus,
    AssessmentType,
    QRCodeType,
    UserRole,
    UserStatus,
    WorkoutStatus,
    WorkoutType,
)


# User Schemas
class UserBase(BaseSchema):
    """Base user schema."""

    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    role: UserRole = UserRole.ATHLETE
    status: UserStatus = UserStatus.ACTIVE


class UserCreate(UserBase):
    """User creation schema."""

    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseSchema):
    """User update schema."""

    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    profile_image_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    height: Optional[float] = Field(None, gt=0)  # in cm
    weight: Optional[float] = Field(None, gt=0)  # in kg


class UserResponse(UserBase):
    """User response schema."""

    id: str
    profile_image_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    created_at: datetime
    updated_at: datetime


# Workout Schemas
class ExerciseBase(BaseSchema):
    """Base exercise schema."""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    category: str = Field(..., min_length=1, max_length=50)
    muscle_groups: List[str] = Field(default_factory=list)
    equipment: Optional[List[str]] = None
    instructions: Optional[str] = None
    video_url: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    """Exercise creation schema."""

    pass


class ExerciseUpdate(BaseSchema):
    """Exercise update schema."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    muscle_groups: Optional[List[str]] = None
    equipment: Optional[List[str]] = None
    instructions: Optional[str] = None
    video_url: Optional[str] = None


class ExerciseResponse(ExerciseBase):
    """Exercise response schema."""

    id: str


class SetBase(BaseSchema):
    """Base set schema."""

    exercise_id: str
    reps: Optional[int] = Field(None, gt=0)
    weight: Optional[float] = Field(None, gt=0)  # in kg
    duration: Optional[int] = Field(None, gt=0)  # in seconds
    distance: Optional[float] = Field(None, gt=0)  # in meters
    rest_time: Optional[int] = Field(None, gt=0)  # in seconds
    notes: Optional[str] = None


class SetCreate(SetBase):
    """Set creation schema."""

    pass


class SetUpdate(BaseSchema):
    """Set update schema."""

    exercise_id: Optional[str] = None
    reps: Optional[int] = Field(None, gt=0)
    weight: Optional[float] = Field(None, gt=0)
    duration: Optional[int] = Field(None, gt=0)
    distance: Optional[float] = Field(None, gt=0)
    rest_time: Optional[int] = Field(None, gt=0)
    notes: Optional[str] = None


class SetResponse(SetBase):
    """Set response schema."""

    id: str


class WorkoutBase(BaseSchema):
    """Base workout schema."""

    user_id: str
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    type: WorkoutType
    status: WorkoutStatus = WorkoutStatus.PLANNED
    scheduled_date: datetime
    duration: Optional[int] = Field(None, gt=0, le=1440)  # in minutes
    notes: Optional[str] = None


class WorkoutCreate(WorkoutBase):
    """Workout creation schema."""

    sets: List[SetCreate] = Field(default_factory=list)


class WorkoutUpdate(BaseSchema):
    """Workout update schema."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    type: Optional[WorkoutType] = None
    status: Optional[WorkoutStatus] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    duration: Optional[int] = Field(None, gt=0, le=1440)
    notes: Optional[str] = None


class WorkoutResponse(WorkoutBase):
    """Workout response schema."""

    id: str
    completed_date: Optional[datetime] = None
    sets: List[SetResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


# Assessment Schemas
class AssessmentBase(BaseSchema):
    """Base assessment schema."""

    user_id: str
    type: AssessmentType
    status: AssessmentStatus = AssessmentStatus.PENDING
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    questions: List[Dict[str, Any]] = Field(default_factory=list)
    scheduled_date: Optional[datetime] = None


class AssessmentCreate(AssessmentBase):
    """Assessment creation schema."""

    pass


class AssessmentUpdate(BaseSchema):
    """Assessment update schema."""

    type: Optional[AssessmentType] = None
    status: Optional[AssessmentStatus] = None
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    questions: Optional[List[Dict[str, Any]]] = None
    answers: Optional[List[Dict[str, Any]]] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None


class AssessmentResultBase(BaseSchema):
    """Base assessment result schema."""

    assessment_id: str
    score: float = Field(..., ge=0, le=100)
    category: str
    details: Dict[str, Any] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)
    ai_analysis: Optional[str] = None


class AssessmentResultCreate(AssessmentResultBase):
    """Assessment result creation schema."""

    pass


class AssessmentResultResponse(AssessmentResultBase):
    """Assessment result response schema."""

    id: str
    created_at: datetime


class AssessmentResponse(AssessmentBase):
    """Assessment response schema."""

    id: str
    answers: Optional[List[Dict[str, Any]]] = None
    result: Optional[AssessmentResultResponse] = None
    completed_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


# File Upload Schemas
class FileUploadBase(BaseSchema):
    """Base file upload schema."""

    filename: str
    original_name: str
    mime_type: str
    size: int = Field(..., gt=0)
    url: str


class FileUploadCreate(FileUploadBase):
    """File upload creation schema."""

    uploaded_by: str


class FileUploadResponse(FileUploadBase):
    """File upload response schema."""

    id: str
    uploaded_by: str
    uploaded_at: datetime


# QR Code Schemas
class QRCodeBase(BaseSchema):
    """Base QR code schema."""

    code: str
    type: QRCodeType
    target_id: str
    expires_at: Optional[datetime] = None
    is_active: bool = True


class QRCodeCreate(QRCodeBase):
    """QR code creation schema."""

    pass


class QRCodeUpdate(BaseSchema):
    """QR code update schema."""

    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None


class QRCodeResponse(QRCodeBase):
    """QR code response schema."""

    id: str
    created_at: datetime


# Query Schemas
class FilterSchema(BaseSchema):
    """Filter schema."""

    field: str
    operator: str
    value: Any


class SortSchema(BaseSchema):
    """Sort schema."""

    field: str
    order: str


class QueryParams(PaginationParams):
    """Query parameters schema."""

    sort: Optional[List[SortSchema]] = None
    filter: Optional[List[FilterSchema]] = None
    search: Optional[str] = Field(None, min_length=2, max_length=100)