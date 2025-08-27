"""Workout-related database models."""

from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship

from pyshared.models.enums import WorkoutStatus, WorkoutType

from .base import TimestampedModel


class Exercise(TimestampedModel, table=True):
    """Exercise model."""

    __tablename__ = "exercises"

    id: Optional[str] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: Optional[str] = None
    category: str = Field(max_length=50)
    muscle_groups: List[str] = Field(default_factory=list)
    equipment: Optional[List[str]] = None
    instructions: Optional[str] = None
    video_url: Optional[str] = None

    # Relationships
    sets: list["Set"] = Relationship(back_populates="exercise")


class Set(TimestampedModel, table=True):
    """Set model."""

    __tablename__ = "sets"

    id: Optional[str] = Field(default=None, primary_key=True)
    workout_id: str = Field(foreign_key="workouts.id")
    exercise_id: str = Field(foreign_key="exercises.id")
    reps: Optional[int] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)  # in kg
    duration: Optional[int] = Field(default=None, gt=0)  # in seconds
    distance: Optional[float] = Field(default=None, gt=0)  # in meters
    rest_time: Optional[int] = Field(default=None, gt=0)  # in seconds
    notes: Optional[str] = None

    # Relationships
    workout: "Workout" = Relationship(back_populates="sets")
    exercise: Exercise = Relationship(back_populates="sets")


class Workout(TimestampedModel, table=True):
    """Workout model."""

    __tablename__ = "workouts"

    id: Optional[str] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    name: str = Field(max_length=100)
    description: Optional[str] = None
    type: WorkoutType
    status: WorkoutStatus = Field(default=WorkoutStatus.PLANNED)
    scheduled_date: datetime
    completed_date: Optional[datetime] = None
    duration: Optional[int] = Field(default=None, gt=0, le=1440)  # in minutes
    notes: Optional[str] = None

    # Relationships
    user: "User" = Relationship(back_populates="workouts")
    sets: List[Set] = Relationship(back_populates="workout")