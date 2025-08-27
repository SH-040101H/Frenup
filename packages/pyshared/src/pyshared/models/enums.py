"""Enum definitions for IR FitMark."""

from enum import Enum


class UserRole(str, Enum):
    """User roles."""

    ATHLETE = "athlete"
    COACH = "coach"
    ADMIN = "admin"


class UserStatus(str, Enum):
    """User status."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class WorkoutType(str, Enum):
    """Workout types."""

    STRENGTH = "strength"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"
    SPORTS = "sports"


class WorkoutStatus(str, Enum):
    """Workout status."""

    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AssessmentType(str, Enum):
    """Assessment types."""

    FITNESS = "fitness"
    NUTRITION = "nutrition"
    MENTAL_HEALTH = "mental_health"
    INJURY_RISK = "injury_risk"


class AssessmentStatus(str, Enum):
    """Assessment status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class QRCodeType(str, Enum):
    """QR code types."""

    WORKOUT = "workout"
    ASSESSMENT = "assessment"
    PROFILE = "profile"


class FileType(str, Enum):
    """File types."""

    IMAGE = "image"
    DOCUMENT = "document"
    VIDEO = "video"


class SortOrder(str, Enum):
    """Sort order."""

    ASC = "asc"
    DESC = "desc"


class FilterOperator(str, Enum):
    """Filter operators."""

    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NIN = "nin"
    LIKE = "like"


class Environment(str, Enum):
    """Environment types."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"