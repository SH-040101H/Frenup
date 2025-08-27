"""Report generation and management endpoints."""

from typing import Any, Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_db, report as crud_report
from pyshared import (
    ApiResponse,
    PaginatedResponse,
    Report,
    ReportCreate,
    ReportPeriod,
)

from ...core.deps import (
    get_current_active_user,
    get_pagination,
    get_filter_params,
    require_instructor_or_admin,
    validate_uuid,
    PaginationParams,
    FilterParams,
)
from ...core.exceptions import NotFoundError

router = APIRouter()


@router.post("/generate", response_model=ApiResponse[Report])
async def generate_report(
    user_id: str,
    period: ReportPeriod,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_instructor_or_admin)
) -> Dict[str, Any]:
    """Generate a new report for a user."""
    
    user_uuid = validate_uuid(user_id, "user_id")
    
    # TODO: Implement actual report generation logic
    # For now, create a basic report structure
    
    from datetime import datetime, timedelta
    
    # Calculate date range based on period
    end_date = datetime.utcnow()
    if period == ReportPeriod.WEEKLY:
        start_date = end_date - timedelta(weeks=1)
    elif period == ReportPeriod.MONTHLY:
        start_date = end_date - timedelta(days=30)
    else:  # QUARTERLY
        start_date = end_date - timedelta(days=90)
    
    # Mock report data
    report_data = {
        "period": period.value,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "summary": {
            "total_assessments": 0,
            "average_score": 0,
            "improvement": 0,
        },
        "assessments": [],
        "recommendations": [],
    }
    
    report_create = ReportCreate(
        user_id=user_uuid,
        period=period,
        data=report_data,
        start_date=start_date,
        end_date=end_date,
    )
    
    report = await crud_report.create(db, report_create)
    
    return {
        "success": True,
        "data": report,
        "message": "Report generated successfully"
    }


@router.get("/", response_model=ApiResponse[PaginatedResponse[Report]])
async def get_reports(
    pagination: PaginationParams = Depends(get_pagination),
    filters: FilterParams = Depends(get_filter_params),
    period: ReportPeriod = Query(None),
    user_id: str = Query(None),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get paginated list of reports."""
    
    # Build filter conditions
    filter_dict = {}
    
    # Students can only see their own reports
    if current_user.role == "student":
        filter_dict["user_id"] = current_user.id
    elif user_id:
        filter_dict["user_id"] = validate_uuid(user_id, "user_id")
    
    if period:
        filter_dict["period"] = period
    
    # Get reports
    if period:
        reports = await crud_report.get_by_period(
            db, period, pagination.offset, pagination.limit
        )
    else:
        reports = await crud_report.get_multi(
            db, pagination.offset, pagination.limit, filter_dict
        )
    
    total = await crud_report.count(db, filter_dict)
    
    # Create paginated response
    paginated_data = {
        "items": reports,
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
        "message": f"Retrieved {len(reports)} reports"
    }


@router.get("/{report_id}", response_model=ApiResponse[Report])
async def get_report(
    report_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get report by ID."""
    
    report_uuid = validate_uuid(report_id, "report_id")
    
    report = await crud_report.get(db, report_uuid)
    if not report:
        raise NotFoundError("Report not found")
    
    # Students can only access their own reports
    if current_user.role == "student" and report.user_id != current_user.id:
        raise NotFoundError("Report not found")
    
    return {
        "success": True,
        "data": report,
        "message": "Report retrieved successfully"
    }


@router.delete("/{report_id}")
async def delete_report(
    report_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_instructor_or_admin)
) -> Dict[str, Any]:
    """Delete report by ID (instructors and admins only)."""
    
    report_uuid = validate_uuid(report_id, "report_id")
    
    success = await crud_report.delete(db, report_uuid)
    if not success:
        raise NotFoundError("Report not found")
    
    return {
        "success": True,
        "message": "Report deleted successfully"
    }


@router.get("/user/{user_id}", response_model=ApiResponse[List[Report]])
async def get_user_reports(
    user_id: str,
    period: ReportPeriod = Query(None),
    pagination: PaginationParams = Depends(get_pagination),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get reports for a specific user."""
    
    user_uuid = validate_uuid(user_id, "user_id")
    
    # Students can only access their own reports
    if current_user.role == "student" and user_uuid != current_user.id:
        raise NotFoundError("User not found")
    
    reports = await crud_report.get_by_user(
        db, user_uuid, pagination.offset, pagination.limit
    )
    
    # Filter by period if specified
    if period:
        reports = [r for r in reports if r.period == period]
    
    return {
        "success": True,
        "data": reports,
        "message": f"Retrieved {len(reports)} reports for user"
    }


@router.get("/{report_id}/download")
async def download_report(
    report_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get download URL for report PDF."""
    
    report_uuid = validate_uuid(report_id, "report_id")
    
    report = await crud_report.get(db, report_uuid)
    if not report:
        raise NotFoundError("Report not found")
    
    # Students can only download their own reports
    if current_user.role == "student" and report.user_id != current_user.id:
        raise NotFoundError("Report not found")
    
    if not report.pdf_url:
        return {
            "success": False,
            "error": "Report PDF not available",
            "message": "Report is still being generated or PDF generation failed"
        }
    
    return {
        "success": True,
        "data": {"download_url": report.pdf_url},
        "message": "Download URL retrieved successfully"
    }


@router.get("/stats/summary")
async def get_report_stats(
    user_id: str = Query(None),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get report statistics."""
    
    # Students can only see their own stats
    if current_user.role == "student":
        target_user_id = current_user.id
    elif user_id:
        target_user_id = validate_uuid(user_id, "user_id")
    else:
        target_user_id = None
    
    # Build filter for user
    filter_dict = {}
    if target_user_id:
        filter_dict["user_id"] = target_user_id
    
    # Get counts by period
    total_reports = await crud_report.count(db, filter_dict)
    weekly_count = await crud_report.count(db, {**filter_dict, "period": "weekly"})
    monthly_count = await crud_report.count(db, {**filter_dict, "period": "monthly"})
    quarterly_count = await crud_report.count(db, {**filter_dict, "period": "quarterly"})
    
    stats = {
        "total_reports": total_reports,
        "by_period": {
            "weekly": weekly_count,
            "monthly": monthly_count,
            "quarterly": quarterly_count,
        }
    }
    
    return {
        "success": True,
        "data": stats,
        "message": "Report statistics retrieved successfully"
    }