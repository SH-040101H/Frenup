"""CRUD operations for database models."""

from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from uuid import UUID

from sqlalchemy import and_, desc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlmodel import SQLModel

from .models import (
    User,
    FitnessAssessment,
    Report,
    QRCode,
    SystemLog,
    Exception as ExceptionModel,
    FileUpload,
    WorkerJob,
)

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDBase:
    """Base CRUD class with common operations."""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    async def get(self, db: AsyncSession, id: UUID) -> Optional[ModelType]:
        """Get a single record by ID."""
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()
    
    async def get_multi(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
    ) -> List[ModelType]:
        """Get multiple records with pagination and filtering."""
        query = select(self.model)
        
        # Apply filters
        if filters:
            filter_conditions = []
            for key, value in filters.items():
                if hasattr(self.model, key):
                    filter_conditions.append(getattr(self.model, key) == value)
            if filter_conditions:
                query = query.where(and_(*filter_conditions))
        
        # Apply ordering
        if order_by and hasattr(self.model, order_by):
            query = query.order_by(desc(getattr(self.model, order_by)))
        else:
            query = query.order_by(desc(self.model.created_at))
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record."""
        if isinstance(obj_in, dict):
            db_obj = self.model(**obj_in)
        else:
            db_obj = self.model.model_validate(obj_in)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing record."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, id: UUID) -> bool:
        """Delete a record by ID."""
        db_obj = await self.get(db, id)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
            return True
        return False
    
    async def count(
        self,
        db: AsyncSession,
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """Count records with optional filtering."""
        query = select(self.model)
        
        if filters:
            filter_conditions = []
            for key, value in filters.items():
                if hasattr(self.model, key):
                    filter_conditions.append(getattr(self.model, key) == value)
            if filter_conditions:
                query = query.where(and_(*filter_conditions))
        
        result = await db.execute(query)
        return len(result.scalars().all())


class CRUDUser(CRUDBase[User]):
    """CRUD operations for User model."""
    
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email."""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_active_users(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Get active users."""
        result = await db.execute(
            select(User)
            .where(User.is_active == True)
            .offset(skip)
            .limit(limit)
            .order_by(desc(User.created_at))
        )
        return result.scalars().all()
    
    async def search_users(
        self,
        db: AsyncSession,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Search users by name or email."""
        result = await db.execute(
            select(User)
            .where(
                or_(
                    User.name.ilike(f"%{search_term}%"),
                    User.email.ilike(f"%{search_term}%")
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(desc(User.created_at))
        )
        return result.scalars().all()


class CRUDFitnessAssessment(CRUDBase[FitnessAssessment]):
    """CRUD operations for FitnessAssessment model."""
    
    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[FitnessAssessment]:
        """Get assessments by user ID."""
        result = await db.execute(
            select(FitnessAssessment)
            .where(FitnessAssessment.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(desc(FitnessAssessment.assessed_at))
        )
        return result.scalars().all()
    
    async def get_by_type_and_user(
        self,
        db: AsyncSession,
        user_id: UUID,
        assessment_type: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[FitnessAssessment]:
        """Get assessments by type and user."""
        result = await db.execute(
            select(FitnessAssessment)
            .where(
                and_(
                    FitnessAssessment.user_id == user_id,
                    FitnessAssessment.assessment_type == assessment_type
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(desc(FitnessAssessment.assessed_at))
        )
        return result.scalars().all()
    
    async def get_pending_assessments(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[FitnessAssessment]:
        """Get pending assessments for processing."""
        result = await db.execute(
            select(FitnessAssessment)
            .where(FitnessAssessment.status == "pending")
            .offset(skip)
            .limit(limit)
            .order_by(FitnessAssessment.created_at)
        )
        return result.scalars().all()


class CRUDReport(CRUDBase[Report]):
    """CRUD operations for Report model."""
    
    async def get_by_user(
        self,
        db: AsyncSession,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Report]:
        """Get reports by user ID."""
        result = await db.execute(
            select(Report)
            .where(Report.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(desc(Report.generated_at))
        )
        return result.scalars().all()
    
    async def get_by_period(
        self,
        db: AsyncSession,
        period: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Report]:
        """Get reports by period."""
        result = await db.execute(
            select(Report)
            .where(Report.period == period)
            .offset(skip)
            .limit(limit)
            .order_by(desc(Report.generated_at))
        )
        return result.scalars().all()


class CRUDQRCode(CRUDBase[QRCode]):
    """CRUD operations for QRCode model."""
    
    async def get_by_code(self, db: AsyncSession, code: str) -> Optional[QRCode]:
        """Get QR code by code string."""
        result = await db.execute(select(QRCode).where(QRCode.code == code))
        return result.scalar_one_or_none()
    
    async def get_active_codes(
        self,
        db: AsyncSession,
        user_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[QRCode]:
        """Get active QR codes."""
        query = select(QRCode).where(QRCode.is_active == True)
        
        if user_id:
            query = query.where(QRCode.user_id == user_id)
        
        result = await db.execute(
            query.offset(skip).limit(limit).order_by(desc(QRCode.created_at))
        )
        return result.scalars().all()
    
    async def increment_usage(self, db: AsyncSession, qr_code: QRCode) -> QRCode:
        """Increment QR code usage count."""
        qr_code.usage_count += 1
        
        # Deactivate if max usage reached
        if qr_code.usage_count >= qr_code.max_usage:
            qr_code.is_active = False
        
        db.add(qr_code)
        await db.commit()
        await db.refresh(qr_code)
        return qr_code


class CRUDSystemLog(CRUDBase[SystemLog]):
    """CRUD operations for SystemLog model."""
    
    async def get_by_component(
        self,
        db: AsyncSession,
        component: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[SystemLog]:
        """Get logs by component."""
        result = await db.execute(
            select(SystemLog)
            .where(SystemLog.component == component)
            .offset(skip)
            .limit(limit)
            .order_by(desc(SystemLog.created_at))
        )
        return result.scalars().all()
    
    async def get_by_level(
        self,
        db: AsyncSession,
        level: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[SystemLog]:
        """Get logs by level."""
        result = await db.execute(
            select(SystemLog)
            .where(SystemLog.level == level)
            .offset(skip)
            .limit(limit)
            .order_by(desc(SystemLog.created_at))
        )
        return result.scalars().all()


class CRUDException(CRUDBase[ExceptionModel]):
    """CRUD operations for Exception model."""
    
    async def get_unresolved(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[ExceptionModel]:
        """Get unresolved exceptions."""
        result = await db.execute(
            select(ExceptionModel)
            .where(ExceptionModel.is_resolved == False)
            .offset(skip)
            .limit(limit)
            .order_by(desc(ExceptionModel.created_at))
        )
        return result.scalars().all()
    
    async def mark_resolved(
        self,
        db: AsyncSession,
        exception_id: UUID,
        resolved_by: str
    ) -> Optional[ExceptionModel]:
        """Mark exception as resolved."""
        exception = await self.get(db, exception_id)
        if exception:
            exception.is_resolved = True
            exception.resolved_by = resolved_by
            exception.resolved_at = datetime.utcnow()
            
            db.add(exception)
            await db.commit()
            await db.refresh(exception)
        
        return exception


class CRUDFileUpload(CRUDBase[FileUpload]):
    """CRUD operations for FileUpload model."""
    
    async def get_by_hash(self, db: AsyncSession, file_hash: str) -> Optional[FileUpload]:
        """Get file upload by hash."""
        result = await db.execute(
            select(FileUpload).where(FileUpload.file_hash == file_hash)
        )
        return result.scalar_one_or_none()
    
    async def get_unprocessed(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[FileUpload]:
        """Get unprocessed files."""
        result = await db.execute(
            select(FileUpload)
            .where(FileUpload.is_processed == False)
            .offset(skip)
            .limit(limit)
            .order_by(FileUpload.created_at)
        )
        return result.scalars().all()


class CRUDWorkerJob(CRUDBase[WorkerJob]):
    """CRUD operations for WorkerJob model."""
    
    async def get_pending_jobs(
        self,
        db: AsyncSession,
        job_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[WorkerJob]:
        """Get pending jobs."""
        query = select(WorkerJob).where(WorkerJob.status == "pending")
        
        if job_type:
            query = query.where(WorkerJob.job_type == job_type)
        
        result = await db.execute(
            query.offset(skip)
            .limit(limit)
            .order_by(WorkerJob.priority, WorkerJob.scheduled_at)
        )
        return result.scalars().all()
    
    async def update_job_status(
        self,
        db: AsyncSession,
        job_id: UUID,
        status: str,
        progress: Optional[int] = None,
        result_data: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None
    ) -> Optional[WorkerJob]:
        """Update job status and progress."""
        job = await self.get(db, job_id)
        if job:
            job.status = status
            if progress is not None:
                job.progress = progress
            if result_data is not None:
                job.result = result_data
            if error_message is not None:
                job.error_message = error_message
            
            # Set timestamps
            if status == "running" and not job.started_at:
                job.started_at = datetime.utcnow()
            elif status in ["completed", "failed"]:
                job.completed_at = datetime.utcnow()
            
            db.add(job)
            await db.commit()
            await db.refresh(job)
        
        return job


# Create CRUD instances
user = CRUDUser(User)
fitness_assessment = CRUDFitnessAssessment(FitnessAssessment)
report = CRUDReport(Report)
qr_code = CRUDQRCode(QRCode)
system_log = CRUDSystemLog(SystemLog)
exception = CRUDException(ExceptionModel)
file_upload = CRUDFileUpload(FileUpload)
worker_job = CRUDWorkerJob(WorkerJob)