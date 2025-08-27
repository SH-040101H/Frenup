"""Assessment-related database models."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlmodel import Field, Relationship

from pyshared.models.enums import AssessmentStatus, AssessmentType

from .base import TimestampedModel


class AssessmentResult(TimestampedModel, table=True):
    """Assessment result model."""

    __tablename__ = "assessment_results"

    id: Optional[str] = Field(default=None, primary_key=True)
    assessment_id: str = Field(foreign_key="assessments.id")
    score: float = Field(ge=0, le=100)
    category: str
    details: Dict[str, Any] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)
    ai_analysis: Optional[str] = None

    # Relationships
    assessment: "Assessment" = Relationship(back_populates="result")


class Assessment(TimestampedModel, table=True):
    """Assessment model."""

    __tablename__ = "assessments"

    id: Optional[str] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    type: AssessmentType
    status: AssessmentStatus = Field(default=AssessmentStatus.PENDING)
    title: str = Field(max_length=200)
    description: Optional[str] = None
    questions: List[Dict[str, Any]] = Field(default_factory=list)
    answers: Optional[List[Dict[str, Any]]] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None

    # Relationships
    user: "User" = Relationship(back_populates="assessments")
    result: Optional[AssessmentResult] = Relationship(back_populates="assessment")