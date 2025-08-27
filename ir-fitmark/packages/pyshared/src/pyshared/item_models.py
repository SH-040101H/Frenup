"""Pydantic models for item tracking in IR FitMark."""

from datetime import date, datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from .models import BaseModelConfig


# Enums that should match the SQLModel definitions
from enum import Enum

class ItemType(str, Enum):
    """Item type enumeration."""
    ERC = "ERC"
    PAD = "PAD"
    LINER = "LINER"
    SLEEPER = "SLEEPER"
    OTHER = "OTHER"


class InspectionStage(str, Enum):
    """Inspection stage enumeration."""
    MFG = "MFG"
    SUPPLY = "SUPPLY"
    INSTALL = "INSTALL"
    PERIODIC = "PERIODIC"
    FAILURE = "FAILURE"


class InspectionOutcome(str, Enum):
    """Inspection outcome enumeration."""
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class InspectionSource(str, Enum):
    """Inspection source enumeration."""
    UDM = "UDM"
    TMS = "TMS"
    MANUAL = "MANUAL"


class ExceptionSeverity(str, Enum):
    """Exception severity enumeration."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ExceptionStatus(str, Enum):
    """Exception status enumeration."""
    OPEN = "OPEN"
    ACK = "ACK"
    CLOSED = "CLOSED"


# Item Models
class ItemBase(BaseModelConfig):
    """Base item model."""
    short_id: str = Field(..., min_length=1, max_length=20)
    type: ItemType
    vendor_id: str = Field(..., min_length=1, max_length=50)
    plant_code: str = Field(..., max_length=20)
    lot: str = Field(..., min_length=1, max_length=50)
    mfg_date: date
    serial: str = Field(..., min_length=1, max_length=100)
    spec_rev: str = Field(..., max_length=20)


class ItemCreate(ItemBase):
    """Item creation model."""
    pass


class ItemUpdate(BaseModelConfig):
    """Item update model."""
    short_id: Optional[str] = Field(None, min_length=1, max_length=20)
    type: Optional[ItemType] = None
    vendor_id: Optional[str] = Field(None, min_length=1, max_length=50)
    plant_code: Optional[str] = Field(None, max_length=20)
    lot: Optional[str] = Field(None, min_length=1, max_length=50)
    mfg_date: Optional[date] = None
    serial: Optional[str] = Field(None, min_length=1, max_length=100)
    spec_rev: Optional[str] = Field(None, max_length=20)


class Item(ItemBase):
    """Item model."""
    id: UUID
    created_at: datetime
    updated_at: datetime


# Warranty Models
class WarrantyBase(BaseModelConfig):
    """Base warranty model."""
    item_id: UUID
    start_date: date
    end_date: date
    terms: str = Field(..., min_length=1)


class WarrantyCreate(WarrantyBase):
    """Warranty creation model."""
    pass


class WarrantyUpdate(BaseModelConfig):
    """Warranty update model."""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    terms: Optional[str] = Field(None, min_length=1)


class Warranty(WarrantyBase):
    """Warranty model."""
    id: UUID


# Inspection Models
class InspectionBase(BaseModelConfig):
    """Base inspection model."""
    item_id: UUID
    stage: InspectionStage
    date: datetime
    outcome: InspectionOutcome
    remarks: Optional[str] = None
    source: InspectionSource = InspectionSource.MANUAL


class InspectionCreate(InspectionBase):
    """Inspection creation model."""
    pass


class InspectionUpdate(BaseModelConfig):
    """Inspection update model."""
    stage: Optional[InspectionStage] = None
    date: Optional[datetime] = None
    outcome: Optional[InspectionOutcome] = None
    remarks: Optional[str] = None
    source: Optional[InspectionSource] = None


class Inspection(InspectionBase):
    """Inspection model."""
    id: UUID


# Scan Event Models
class ScanEventBase(BaseModelConfig):
    """Base scan event model."""
    item_id: UUID
    actor_id: str = Field(..., min_length=1, max_length=100)
    lat: Optional[float] = Field(None, ge=-90, le=90)
    lng: Optional[float] = Field(None, ge=-180, le=180)
    photo_url: Optional[str] = Field(None, max_length=500)


class ScanEventCreate(ScanEventBase):
    """Scan event creation model."""
    pass


class ScanEvent(ScanEventBase):
    """Scan event model."""
    id: UUID
    scanned_at: datetime


# Exception Models
class ItemExceptionBase(BaseModelConfig):
    """Base item exception model."""
    item_id: UUID
    code: str = Field(..., min_length=1, max_length=50)
    severity: ExceptionSeverity
    message: str = Field(..., min_length=1)
    status: ExceptionStatus = ExceptionStatus.OPEN


class ItemExceptionCreate(ItemExceptionBase):
    """Item exception creation model."""
    pass


class ItemExceptionUpdate(BaseModelConfig):
    """Item exception update model."""
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    severity: Optional[ExceptionSeverity] = None
    message: Optional[str] = Field(None, min_length=1)
    status: Optional[ExceptionStatus] = None


class ItemException(ItemExceptionBase):
    """Item exception model."""
    id: UUID
    created_at: datetime
    updated_at: datetime


# Composite Models
class ItemWithRelations(Item):
    """Item model with related data."""
    warranties: List[Warranty] = []
    latest_inspection: Optional[Inspection] = None
    recent_scans: List[ScanEvent] = []
    open_exceptions: List[ItemException] = []


class InspectionSummary(BaseModelConfig):
    """Inspection summary model."""
    total_inspections: int
    passed: int
    warned: int
    failed: int
    by_stage: dict[str, int]
    latest_date: Optional[datetime] = None


class ItemStats(BaseModelConfig):
    """Item statistics model."""
    total_items: int
    by_type: dict[str, int]
    by_vendor: dict[str, int]
    items_with_warranty: int
    items_with_exceptions: int
    recent_scans_count: int


# Search and Filter Models
class ItemSearchParams(BaseModelConfig):
    """Item search parameters."""
    search: Optional[str] = None
    type: Optional[ItemType] = None
    vendor_id: Optional[str] = None
    lot: Optional[str] = None
    serial: Optional[str] = None
    has_warranty: Optional[bool] = None
    has_exceptions: Optional[bool] = None


class InspectionSearchParams(BaseModelConfig):
    """Inspection search parameters."""
    item_id: Optional[UUID] = None
    stage: Optional[InspectionStage] = None
    outcome: Optional[InspectionOutcome] = None
    source: Optional[InspectionSource] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None


class ExceptionSearchParams(BaseModelConfig):
    """Exception search parameters."""
    item_id: Optional[UUID] = None
    severity: Optional[ExceptionSeverity] = None
    status: Optional[ExceptionStatus] = None
    code: Optional[str] = None