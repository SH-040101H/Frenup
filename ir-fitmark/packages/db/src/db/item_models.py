"""SQLModel database models for Item Tracking in IR FitMark."""

from datetime import date, datetime
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship, Column, JSON, Index
from sqlalchemy import DateTime, Date, func, Float, Text

from .models import TimestampMixin


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


class Item(TimestampMixin, table=True):
    """Item model for tracking components."""
    __tablename__ = "items"
    
    # Primary identifiers
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    short_id: str = Field(unique=True, index=True, max_length=20)
    
    # Item classification
    type: ItemType = Field(index=True)
    
    # Manufacturing details
    vendor_id: str = Field(index=True, max_length=50)
    plant_code: str = Field(max_length=20)
    lot: str = Field(index=True, max_length=50)
    mfg_date: date = Field(sa_column=Column(Date))
    serial: str = Field(index=True, max_length=100)
    spec_rev: str = Field(max_length=20)
    
    # Relationships
    warranties: List["Warranty"] = Relationship(back_populates="item")
    inspections: List["Inspection"] = Relationship(back_populates="item")
    scan_events: List["ScanEvent"] = Relationship(back_populates="item")
    exceptions: List["Exception"] = Relationship(back_populates="item")


class Warranty(SQLModel, table=True):
    """Warranty model for items."""
    __tablename__ = "warranties"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    item_id: UUID = Field(foreign_key="items.id", index=True)
    start_date: date = Field(sa_column=Column(Date))
    end_date: date = Field(sa_column=Column(Date))
    terms: str = Field(sa_column=Column(Text))
    
    # Relationships
    item: Item = Relationship(back_populates="warranties")


class Inspection(SQLModel, table=True):
    """Inspection model for tracking item inspections."""
    __tablename__ = "inspections"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    item_id: UUID = Field(foreign_key="items.id", index=True)
    stage: InspectionStage = Field(index=True)
    date: datetime = Field(sa_column=Column(DateTime(timezone=True)), index=True)
    outcome: InspectionOutcome = Field(index=True)
    remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    source: InspectionSource = Field(default=InspectionSource.MANUAL)
    
    # Relationships
    item: Item = Relationship(back_populates="inspections")
    
    # Composite index for item_id + date for efficient querying
    __table_args__ = (
        Index('ix_inspections_item_date', 'item_id', 'date'),
    )


class ScanEvent(SQLModel, table=True):
    """Scan event model for tracking item scans."""
    __tablename__ = "scan_events"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    item_id: UUID = Field(foreign_key="items.id", index=True)
    actor_id: str = Field(max_length=100)  # User or system ID that performed the scan
    scanned_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        index=True
    )
    
    # Optional location data
    lat: Optional[float] = Field(default=None, sa_column=Column(Float))
    lng: Optional[float] = Field(default=None, sa_column=Column(Float))
    
    # Optional photo documentation
    photo_url: Optional[str] = Field(default=None, max_length=500)
    
    # Relationships
    item: Item = Relationship(back_populates="scan_events")


class Exception(TimestampMixin, table=True):
    """Exception model for tracking item issues."""
    __tablename__ = "item_exceptions"  # Using item_exceptions to avoid conflict with Python exception
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    item_id: UUID = Field(foreign_key="items.id", index=True)
    code: str = Field(max_length=50, index=True)
    severity: ExceptionSeverity = Field(index=True)
    message: str = Field(sa_column=Column(Text))
    status: ExceptionStatus = Field(default=ExceptionStatus.OPEN, index=True)
    
    # Relationships
    item: Item = Relationship(back_populates="exceptions")


# Update the main models to include the new tables
def create_item_tables(engine):
    """Create all item tracking tables."""
    SQLModel.metadata.create_all(engine, tables=[
        Item.__table__,
        Warranty.__table__,
        Inspection.__table__,
        ScanEvent.__table__,
        Exception.__table__,
    ])