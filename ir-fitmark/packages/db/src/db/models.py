"""SQLModel database models for IR FitMark."""

from datetime import datetime
from typing import Dict, Any, Optional, List
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from sqlalchemy import DateTime, func

from pyshared import UserRole, AssessmentType, AssessmentStatus, ReportPeriod


class TimestampMixin(SQLModel):
    """Mixin to add timestamp fields."""
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )


class User(TimestampMixin, table=True):
    """User model."""
    __tablename__ = "users"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=100)
    hashed_password: str = Field(max_length=255)
    role: UserRole = Field(default=UserRole.STUDENT)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    
    # Profile information
    age: Optional[int] = Field(default=None, ge=1, le=120)
    gender: Optional[str] = Field(default=None, max_length=20)
    height: Optional[float] = Field(default=None, ge=0)  # in cm
    weight: Optional[float] = Field(default=None, ge=0)  # in kg
    
    # Relationships
    fitness_assessments: List["FitnessAssessment"] = Relationship(back_populates="user")
    reports: List["Report"] = Relationship(back_populates="user")
    qr_codes: List["QRCode"] = Relationship(back_populates="user")


class FitnessAssessment(TimestampMixin, table=True):
    """Fitness assessment model."""
    __tablename__ = "fitness_assessments"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    assessment_type: AssessmentType = Field(index=True)
    
    # Assessment data
    score: float = Field(ge=0, le=100)
    raw_data: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    video_url: Optional[str] = Field(default=None, max_length=500)
    thumbnail_url: Optional[str] = Field(default=None, max_length=500)
    
    # AI processing
    ai_confidence: float = Field(ge=0, le=1)
    ai_model_version: Optional[str] = Field(default=None, max_length=50)
    processing_time: Optional[float] = Field(default=None, ge=0)  # in seconds
    
    # Status and metadata
    status: AssessmentStatus = Field(default=AssessmentStatus.PENDING, index=True)
    error_message: Optional[str] = Field(default=None, max_length=1000)
    assessed_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: User = Relationship(back_populates="fitness_assessments")


class Report(TimestampMixin, table=True):
    """Report model."""
    __tablename__ = "reports"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    period: ReportPeriod = Field(index=True)
    
    # Report data
    data: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    pdf_url: Optional[str] = Field(default=None, max_length=500)
    file_size: Optional[int] = Field(default=None, ge=0)  # in bytes
    
    # Generation metadata
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    generation_time: Optional[float] = Field(default=None, ge=0)  # in seconds
    template_version: Optional[str] = Field(default=None, max_length=50)
    
    # Date range for the report
    start_date: datetime = Field()
    end_date: datetime = Field()
    
    # Relationships
    user: User = Relationship(back_populates="reports")


class QRCode(TimestampMixin, table=True):
    """QR code model."""
    __tablename__ = "qr_codes"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    code: str = Field(unique=True, index=True, max_length=100)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    
    # QR code configuration
    expires_at: datetime = Field(index=True)
    max_usage: int = Field(default=1, ge=1)
    usage_count: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True, index=True)
    
    # QR code type and metadata
    qr_type: str = Field(default="assessment", max_length=50)  # assessment, login, etc.
    metadata: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    
    # Relationships
    user: User = Relationship(back_populates="qr_codes")


class SystemLog(TimestampMixin, table=True):
    """System log model for audit trail."""
    __tablename__ = "system_logs"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    # Log details
    level: str = Field(max_length=20, index=True)  # INFO, WARNING, ERROR, etc.
    message: str = Field(max_length=1000)
    component: str = Field(max_length=100, index=True)  # api, worker, etc.
    
    # Context
    user_id: Optional[UUID] = Field(default=None, index=True)
    session_id: Optional[str] = Field(default=None, max_length=100)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None, max_length=500)
    
    # Additional data
    extra_data: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


class Exception(TimestampMixin, table=True):
    """Exception tracking model."""
    __tablename__ = "exceptions"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    # Exception details
    exception_type: str = Field(max_length=100, index=True)
    message: str = Field(max_length=1000)
    traceback: str = Field()
    
    # Context
    component: str = Field(max_length=100, index=True)
    function_name: Optional[str] = Field(default=None, max_length=100)
    user_id: Optional[UUID] = Field(default=None, index=True)
    
    # Request context
    request_id: Optional[str] = Field(default=None, max_length=100)
    endpoint: Optional[str] = Field(default=None, max_length=200)
    method: Optional[str] = Field(default=None, max_length=10)
    
    # Status
    is_resolved: bool = Field(default=False, index=True)
    resolved_at: Optional[datetime] = Field(default=None)
    resolved_by: Optional[str] = Field(default=None, max_length=100)
    
    # Additional data
    extra_data: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


class FileUpload(TimestampMixin, table=True):
    """File upload tracking model."""
    __tablename__ = "file_uploads"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    
    # File information
    original_filename: str = Field(max_length=255)
    stored_filename: str = Field(max_length=255, unique=True)
    file_path: str = Field(max_length=500)
    file_size: int = Field(ge=0)
    mime_type: str = Field(max_length=100)
    file_hash: str = Field(max_length=64, index=True)
    
    # Upload metadata
    upload_type: str = Field(max_length=50, index=True)  # video, image, document
    purpose: str = Field(max_length=100)  # assessment, profile, report
    
    # Processing status
    is_processed: bool = Field(default=False, index=True)
    processed_at: Optional[datetime] = Field(default=None)
    processing_error: Optional[str] = Field(default=None, max_length=1000)
    
    # S3/Storage information
    s3_bucket: Optional[str] = Field(default=None, max_length=100)
    s3_key: Optional[str] = Field(default=None, max_length=500)
    
    # Relationships
    user: User = Relationship()


class WorkerJob(TimestampMixin, table=True):
    """Worker job tracking model."""
    __tablename__ = "worker_jobs"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    # Job information
    job_type: str = Field(max_length=100, index=True)
    job_name: str = Field(max_length=200)
    job_data: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    
    # Scheduling
    scheduled_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    
    # Status
    status: str = Field(default="pending", index=True)  # pending, running, completed, failed
    progress: int = Field(default=0, ge=0, le=100)
    
    # Results
    result: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    error_message: Optional[str] = Field(default=None, max_length=1000)
    
    # Retry logic
    retry_count: int = Field(default=0, ge=0)
    max_retries: int = Field(default=3, ge=0)
    
    # Priority and worker assignment
    priority: int = Field(default=5, ge=1, le=10)  # 1=highest, 10=lowest
    worker_id: Optional[str] = Field(default=None, max_length=100)


# Create all tables (this will be used by Alembic)
def create_tables(engine):
    """Create all tables."""
    # Import item models to ensure they're registered with SQLModel.metadata
    from .item_models import Item, Warranty, Inspection, ScanEvent, Exception
    SQLModel.metadata.create_all(engine)