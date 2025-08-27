"""Admin dashboard endpoints."""

from typing import Any, Dict, List
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from db import (
    get_async_db,
    user as crud_user,
    fitness_assessment as crud_assessment,
    report as crud_report,
    qr_code as crud_qr,
    exception as crud_exception,
    system_log as crud_log,
    worker_job as crud_job,
)
from pyshared import ApiResponse, PaginatedResponse

from ...core.deps import (
    require_admin,
    get_pagination,
    get_filter_params,
    PaginationParams,
    FilterParams,
)

router = APIRouter()


@router.get("/dashboard", response_model=ApiResponse[Dict[str, Any]])
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_admin)
) -> Dict[str, Any]:
    """Get admin dashboard statistics."""
    
    # User statistics
    total_users = await crud_user.count(db)
    active_users = await crud_user.count(db, {"is_active": True})
    admin_count = await crud_user.count(db, {"role": "admin"})
    instructor_count = await crud_user.count(db, {"role": "instructor"})
    student_count = await crud_user.count(db, {"role": "student"})
    
    # Assessment statistics
    total_assessments = await crud_assessment.count(db)
    pending_assessments = await crud_assessment.count(db, {"status": "pending"})
    processing_assessments = await crud_assessment.count(db, {"status": "processing"})
    completed_assessments = await crud_assessment.count(db, {"status": "completed"})
    failed_assessments = await crud_assessment.count(db, {"status": "failed"})
    
    # Report statistics
    total_reports = await crud_report.count(db)
    weekly_reports = await crud_report.count(db, {"period": "weekly"})
    monthly_reports = await crud_report.count(db, {"period": "monthly"})
    quarterly_reports = await crud_report.count(db, {"period": "quarterly"})
    
    # QR code statistics
    total_qr_codes = await crud_qr.count(db)
    active_qr_codes = await crud_qr.count(db, {"is_active": True})
    
    # Exception statistics
    total_exceptions = await crud_exception.count(db)
    unresolved_exceptions = await crud_exception.count(db, {"is_resolved": False})
    
    # Worker job statistics
    total_jobs = await crud_job.count(db)
    pending_jobs = await crud_job.count(db, {"status": "pending"})
    running_jobs = await crud_job.count(db, {"status": "running"})
    completed_jobs = await crud_job.count(db, {"status": "completed"})
    failed_jobs = await crud_job.count(db, {"status": "failed"})
    
    # Recent activity (last 24 hours)
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_users = await crud_user.count(db, {"created_at__gte": yesterday})
    recent_assessments = await crud_assessment.count(db, {"created_at__gte": yesterday})
    recent_reports = await crud_report.count(db, {"created_at__gte": yesterday})
    
    dashboard_data = {
        "users": {
            "total": total_users,
            "active": active_users,
            "inactive": total_users - active_users,
            "by_role": {
                "admin": admin_count,
                "instructor": instructor_count,
                "student": student_count,
            },
            "recent_registrations": recent_users,
        },
        "assessments": {
            "total": total_assessments,
            "pending": pending_assessments,
            "processing": processing_assessments,
            "completed": completed_assessments,
            "failed": failed_assessments,
            "recent": recent_assessments,
        },
        "reports": {
            "total": total_reports,
            "by_period": {
                "weekly": weekly_reports,
                "monthly": monthly_reports,
                "quarterly": quarterly_reports,
            },
            "recent": recent_reports,
        },
        "qr_codes": {
            "total": total_qr_codes,
            "active": active_qr_codes,
            "inactive": total_qr_codes - active_qr_codes,
        },
        "system_health": {
            "total_exceptions": total_exceptions,
            "unresolved_exceptions": unresolved_exceptions,
            "exception_rate": round(unresolved_exceptions / max(total_exceptions, 1) * 100, 2),
        },
        "worker_jobs": {
            "total": total_jobs,
            "pending": pending_jobs,
            "running": running_jobs,
            "completed": completed_jobs,
            "failed": failed_jobs,
        },
    }
    
    return {
        "success": True,
        "data": dashboard_data,
        "message": "Dashboard statistics retrieved successfully"
    }


@router.get("/exceptions", response_model=ApiResponse[PaginatedResponse])
async def get_exceptions(
    pagination: PaginationParams = Depends(get_pagination),
    filters: FilterParams = Depends(get_filter_params),
    is_resolved: bool = Query(None),
    exception_type: str = Query(None),
    component: str = Query(None),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_admin)
) -> Dict[str, Any]:
    """Get system exceptions for admin review."""
    
    # Build filter conditions
    filter_dict = {}
    
    if is_resolved is not None:
        filter_dict["is_resolved"] = is_resolved
    
    if exception_type:
        filter_dict["exception_type"] = exception_type
    
    if component:
        filter_dict["component"] = component
    
    # Get exceptions
    if is_resolved is False:
        exceptions = await crud_exception.get_unresolved(
            db, pagination.offset, pagination.limit
        )
    else:
        exceptions = await crud_exception.get_multi(
            db, pagination.offset, pagination.limit, filter_dict
        )
    
    total = await crud_exception.count(db, filter_dict)
    
    # Create paginated response
    paginated_data = {
        "items": exceptions,
        "pagination": {
            "page": pagination.page,
            "limit": pagination.limit,
            "total": total,
            "pages": (total + pagination.limit - 1) // pagination.limit,
        }
    }
    
    return {
        "success": True,
        "data": paginated_data,
        "message": f"Retrieved {len(exceptions)} exceptions"
    }


@router.put("/exceptions/{exception_id}/resolve")
async def resolve_exception(
    exception_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_admin)
) -> Dict[str, Any]:
    """Mark an exception as resolved."""
    
    from uuid import UUID
    try:
        exception_uuid = UUID(exception_id)
    except ValueError:
        return {
            "success": False,
            "error": "Invalid exception ID format",
        }
    
    exception = await crud_exception.mark_resolved(
        db, exception_uuid, current_user.email
    )
    
    if not exception:
        return {
            "success": False,
            "error": "Exception not found",
        }
    
    return {
        "success": True,
        "data": exception,
        "message": "Exception marked as resolved"
    }


@router.get("/logs", response_model=ApiResponse[PaginatedResponse])
async def get_system_logs(
    pagination: PaginationParams = Depends(get_pagination),
    level: str = Query(None),
    component: str = Query(None),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_admin)
) -> Dict[str, Any]:
    """Get system logs for admin review."""
    
    # Build filter conditions
    filter_dict = {}
    
    if level:
        filter_dict["level"] = level
    
    if component:
        filter_dict["component"] = component
    
    # Get logs
    if level:
        logs = await crud_log.get_by_level(
            db, level, pagination.offset, pagination.limit
        )
    elif component:
        logs = await crud_log.get_by_component(
            db, component, pagination.offset, pagination.limit
        )
    else:
        logs = await crud_log.get_multi(
            db, pagination.offset, pagination.limit, filter_dict
        )
    
    total = await crud_log.count(db, filter_dict)
    
    # Create paginated response
    paginated_data = {
        "items": logs,
        "pagination": {
            "page": pagination.page,
            "limit": pagination.limit,
            "total": total,
            "pages": (total + pagination.limit - 1) // pagination.limit,
        }
    }
    
    return {
        "success": True,
        "data": paginated_data,
        "message": f"Retrieved {len(logs)} log entries"
    }


@router.get("/worker-jobs", response_model=ApiResponse[PaginatedResponse])
async def get_worker_jobs(
    pagination: PaginationParams = Depends(get_pagination),
    status: str = Query(None),
    job_type: str = Query(None),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_admin)
) -> Dict[str, Any]:
    """Get worker jobs for admin monitoring."""
    
    # Build filter conditions
    filter_dict = {}
    
    if status:
        filter_dict["status"] = status
    
    if job_type:
        filter_dict["job_type"] = job_type
    
    # Get jobs
    if status == "pending":
        jobs = await crud_job.get_pending_jobs(
            db, job_type, pagination.offset, pagination.limit
        )
    else:
        jobs = await crud_job.get_multi(
            db, pagination.offset, pagination.limit, filter_dict
        )
    
    total = await crud_job.count(db, filter_dict)
    
    # Create paginated response
    paginated_data = {
        "items": jobs,
        "pagination": {
            "page": pagination.page,
            "limit": pagination.limit,
            "total": total,
            "pages": (total + pagination.limit - 1) // pagination.limit,
        }
    }
    
    return {
        "success": True,
        "data": paginated_data,
        "message": f"Retrieved {len(jobs)} worker jobs"
    }


@router.get("/system-health")
async def get_system_health(
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_admin)
) -> Dict[str, Any]:
    """Get system health status."""
    
    # Database health
    from db import check_db_health
    db_healthy = await check_db_health()
    
    # Recent error rates
    last_hour = datetime.utcnow() - timedelta(hours=1)
    recent_exceptions = await crud_exception.count(db, {"created_at__gte": last_hour})
    recent_failed_jobs = await crud_job.count(db, {
        "status": "failed",
        "completed_at__gte": last_hour
    })
    
    # Worker job queue health
    pending_jobs = await crud_job.count(db, {"status": "pending"})
    stuck_jobs = await crud_job.count(db, {
        "status": "running",
        "started_at__lt": datetime.utcnow() - timedelta(hours=2)
    })
    
    health_status = {
        "database": {
            "healthy": db_healthy,
            "status": "connected" if db_healthy else "disconnected"
        },
        "error_rates": {
            "exceptions_last_hour": recent_exceptions,
            "failed_jobs_last_hour": recent_failed_jobs,
            "status": "good" if recent_exceptions < 10 and recent_failed_jobs < 5 else "warning"
        },
        "worker_queue": {
            "pending_jobs": pending_jobs,
            "stuck_jobs": stuck_jobs,
            "status": "good" if pending_jobs < 100 and stuck_jobs == 0 else "warning"
        },
        "overall_status": "healthy" if db_healthy and recent_exceptions < 10 and stuck_jobs == 0 else "degraded"
    }
    
    return {
        "success": True,
        "data": health_status,
        "message": "System health status retrieved successfully"
    }