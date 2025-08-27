"""CRUD operations for item tracking models."""

from typing import Any, Dict, List, Optional
from uuid import UUID
from datetime import datetime, date

from sqlalchemy import and_, desc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .crud import CRUDBase
from .item_models import (
    Item,
    Warranty,
    Inspection,
    ScanEvent,
    Exception as ItemException,
    ItemType,
    InspectionStage,
    InspectionOutcome,
    InspectionSource,
    ExceptionSeverity,
    ExceptionStatus,
)


class CRUDItem(CRUDBase[Item]):
    """CRUD operations for Item model."""
    
    async def get_by_short_id(self, db: AsyncSession, short_id: str) -> Optional[Item]:
        """Get item by short ID."""
        result = await db.execute(select(Item).where(Item.short_id == short_id))
        return result.scalar_one_or_none()
    
    async def get_by_serial(self, db: AsyncSession, serial: str) -> Optional[Item]:
        """Get item by serial number."""
        result = await db.execute(select(Item).where(Item.serial == serial))
        return result.scalar_one_or_none()
    
    async def get_by_vendor_and_lot(
        self,
        db: AsyncSession,
        vendor_id: str,
        lot: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Item]:
        """Get items by vendor ID and lot."""
        result = await db.execute(
            select(Item)
            .where(and_(Item.vendor_id == vendor_id, Item.lot == lot))
            .offset(skip)
            .limit(limit)
            .order_by(desc(Item.created_at))
        )
        return result.scalars().all()
    
    async def get_by_type(
        self,
        db: AsyncSession,
        item_type: ItemType,
        skip: int = 0,
        limit: int = 100
    ) -> List[Item]:
        """Get items by type."""
        result = await db.execute(
            select(Item)
            .where(Item.type == item_type)
            .offset(skip)
            .limit(limit)
            .order_by(desc(Item.created_at))
        )
        return result.scalars().all()
    
    async def search_items(
        self,
        db: AsyncSession,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Item]:
        """Search items by serial, short_id, vendor_id, or lot."""
        result = await db.execute(
            select(Item)
            .where(
                or_(
                    Item.serial.ilike(f"%{search_term}%"),
                    Item.short_id.ilike(f"%{search_term}%"),
                    Item.vendor_id.ilike(f"%{search_term}%"),
                    Item.lot.ilike(f"%{search_term}%")
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(desc(Item.created_at))
        )
        return result.scalars().all()


class CRUDWarranty(CRUDBase[Warranty]):
    """CRUD operations for Warranty model."""
    
    async def get_by_item(
        self,
        db: AsyncSession,
        item_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Warranty]:
        """Get warranties by item ID."""
        result = await db.execute(
            select(Warranty)
            .where(Warranty.item_id == item_id)
            .offset(skip)
            .limit(limit)
            .order_by(desc(Warranty.start_date))
        )
        return result.scalars().all()
    
    async def get_active_warranty(
        self,
        db: AsyncSession,
        item_id: UUID,
        check_date: Optional[date] = None
    ) -> Optional[Warranty]:
        """Get active warranty for an item on a specific date."""
        if check_date is None:
            check_date = date.today()
        
        result = await db.execute(
            select(Warranty)
            .where(
                and_(
                    Warranty.item_id == item_id,
                    Warranty.start_date <= check_date,
                    Warranty.end_date >= check_date
                )
            )
            .order_by(desc(Warranty.start_date))
            .limit(1)
        )
        return result.scalar_one_or_none()


class CRUDInspection(CRUDBase[Inspection]):
    """CRUD operations for Inspection model."""
    
    async def get_by_item(
        self,
        db: AsyncSession,
        item_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Inspection]:
        """Get inspections by item ID."""
        result = await db.execute(
            select(Inspection)
            .where(Inspection.item_id == item_id)
            .offset(skip)
            .limit(limit)
            .order_by(desc(Inspection.date))
        )
        return result.scalars().all()
    
    async def get_by_stage(
        self,
        db: AsyncSession,
        stage: InspectionStage,
        skip: int = 0,
        limit: int = 100
    ) -> List[Inspection]:
        """Get inspections by stage."""
        result = await db.execute(
            select(Inspection)
            .where(Inspection.stage == stage)
            .offset(skip)
            .limit(limit)
            .order_by(desc(Inspection.date))
        )
        return result.scalars().all()
    
    async def get_by_outcome(
        self,
        db: AsyncSession,
        outcome: InspectionOutcome,
        skip: int = 0,
        limit: int = 100
    ) -> List[Inspection]:
        """Get inspections by outcome."""
        result = await db.execute(
            select(Inspection)
            .where(Inspection.outcome == outcome)
            .offset(skip)
            .limit(limit)
            .order_by(desc(Inspection.date))
        )
        return result.scalars().all()
    
    async def get_latest_by_item(
        self,
        db: AsyncSession,
        item_id: UUID
    ) -> Optional[Inspection]:
        """Get the latest inspection for an item."""
        result = await db.execute(
            select(Inspection)
            .where(Inspection.item_id == item_id)
            .order_by(desc(Inspection.date))
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    async def get_failed_inspections(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[Inspection]:
        """Get all failed inspections."""
        result = await db.execute(
            select(Inspection)
            .where(Inspection.outcome == InspectionOutcome.FAIL)
            .offset(skip)
            .limit(limit)
            .order_by(desc(Inspection.date))
        )
        return result.scalars().all()


class CRUDScanEvent(CRUDBase[ScanEvent]):
    """CRUD operations for ScanEvent model."""
    
    async def get_by_item(
        self,
        db: AsyncSession,
        item_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[ScanEvent]:
        """Get scan events by item ID."""
        result = await db.execute(
            select(ScanEvent)
            .where(ScanEvent.item_id == item_id)
            .offset(skip)
            .limit(limit)
            .order_by(desc(ScanEvent.scanned_at))
        )
        return result.scalars().all()
    
    async def get_by_actor(
        self,
        db: AsyncSession,
        actor_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[ScanEvent]:
        """Get scan events by actor ID."""
        result = await db.execute(
            select(ScanEvent)
            .where(ScanEvent.actor_id == actor_id)
            .offset(skip)
            .limit(limit)
            .order_by(desc(ScanEvent.scanned_at))
        )
        return result.scalars().all()
    
    async def get_recent_scans(
        self,
        db: AsyncSession,
        hours: int = 24,
        skip: int = 0,
        limit: int = 100
    ) -> List[ScanEvent]:
        """Get recent scan events within specified hours."""
        from datetime import timedelta
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        result = await db.execute(
            select(ScanEvent)
            .where(ScanEvent.scanned_at >= cutoff_time)
            .offset(skip)
            .limit(limit)
            .order_by(desc(ScanEvent.scanned_at))
        )
        return result.scalars().all()


class CRUDItemException(CRUDBase[ItemException]):
    """CRUD operations for ItemException model."""
    
    async def get_by_item(
        self,
        db: AsyncSession,
        item_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[ItemException]:
        """Get exceptions by item ID."""
        result = await db.execute(
            select(ItemException)
            .where(ItemException.item_id == item_id)
            .offset(skip)
            .limit(limit)
            .order_by(desc(ItemException.created_at))
        )
        return result.scalars().all()
    
    async def get_by_severity(
        self,
        db: AsyncSession,
        severity: ExceptionSeverity,
        skip: int = 0,
        limit: int = 100
    ) -> List[ItemException]:
        """Get exceptions by severity."""
        result = await db.execute(
            select(ItemException)
            .where(ItemException.severity == severity)
            .offset(skip)
            .limit(limit)
            .order_by(desc(ItemException.created_at))
        )
        return result.scalars().all()
    
    async def get_open_exceptions(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[ItemException]:
        """Get open exceptions."""
        result = await db.execute(
            select(ItemException)
            .where(ItemException.status == ExceptionStatus.OPEN)
            .offset(skip)
            .limit(limit)
            .order_by(desc(ItemException.created_at))
        )
        return result.scalars().all()
    
    async def get_critical_exceptions(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[ItemException]:
        """Get critical severity exceptions."""
        result = await db.execute(
            select(ItemException)
            .where(ItemException.severity == ExceptionSeverity.CRITICAL)
            .offset(skip)
            .limit(limit)
            .order_by(desc(ItemException.created_at))
        )
        return result.scalars().all()
    
    async def update_status(
        self,
        db: AsyncSession,
        exception_id: UUID,
        status: ExceptionStatus
    ) -> Optional[ItemException]:
        """Update exception status."""
        exception = await self.get(db, exception_id)
        if exception:
            exception.status = status
            db.add(exception)
            await db.commit()
            await db.refresh(exception)
        return exception


# Create CRUD instances
item = CRUDItem(Item)
warranty = CRUDWarranty(Warranty)
inspection = CRUDInspection(Inspection)
scan_event = CRUDScanEvent(ScanEvent)
item_exception = CRUDItemException(ItemException)