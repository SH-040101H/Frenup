"""Fitness assessment endpoints."""

from typing import Any, Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_db, fitness_assessment as crud_assessment
from pyshared import (
    ApiResponse,
    PaginatedResponse,
    FitnessAssessment,
    FitnessAssessmentCreate,
    FitnessAssessmentUpdate,
    AssessmentType,
    AssessmentStatus,
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
from ...core.exceptions import NotFoundError, ValidationError

router = APIRouter()


@router.post("/", response_model=ApiResponse[FitnessAssessment])
async def create_assessment(
    assessment_data: FitnessAssessmentCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Create a new fitness assessment."""
    
    # Set user_id to current user if not provided or if not admin/instructor
    if current_user.role == "student":
        assessment_data.user_id = current_user.id
    
    assessment = await crud_assessment.create(db, assessment_data)
    
    return {
        "success": True,
        "data": assessment,
        "message": "Assessment created successfully"
    }


@router.get("/", response_model=ApiResponse[PaginatedResponse[FitnessAssessment]])
async def get_assessments(
    pagination: PaginationParams = Depends(get_pagination),
    filters: FilterParams = Depends(get_filter_params),
    assessment_type: AssessmentType = Query(None),
    status: AssessmentStatus = Query(None),
    user_id: str = Query(None),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get paginated list of assessments."""
    
    # Build filter conditions
    filter_dict = {}
    
    # Students can only see their own assessments
    if current_user.role == "student":
        filter_dict["user_id"] = current_user.id
    elif user_id:
        filter_dict["user_id"] = validate_uuid(user_id, "user_id")
    
    if assessment_type:
        filter_dict["assessment_type"] = assessment_type
    
    if status:
        filter_dict["status"] = status
    
    # Get assessments
    assessments = await crud_assessment.get_multi(
        db, pagination.offset, pagination.limit, filter_dict
    )
    total = await crud_assessment.count(db, filter_dict)
    
    # Create paginated response
    paginated_data = {
        "items": assessments,
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
        "message": f"Retrieved {len(assessments)} assessments"
    }


@router.get("/{assessment_id}", response_model=ApiResponse[FitnessAssessment])
async def get_assessment(
    assessment_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get assessment by ID."""
    
    assessment_uuid = validate_uuid(assessment_id, "assessment_id")
    
    assessment = await crud_assessment.get(db, assessment_uuid)
    if not assessment:
        raise NotFoundError("Assessment not found")
    
    # Students can only access their own assessments
    if current_user.role == "student" and assessment.user_id != current_user.id:
        raise NotFoundError("Assessment not found")
    
    return {
        "success": True,
        "data": assessment,
        "message": "Assessment retrieved successfully"
    }


@router.put("/{assessment_id}", response_model=ApiResponse[FitnessAssessment])
async def update_assessment(
    assessment_id: str,
    assessment_update: FitnessAssessmentUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_instructor_or_admin)
) -> Dict[str, Any]:
    """Update assessment by ID (instructors and admins only)."""
    
    assessment_uuid = validate_uuid(assessment_id, "assessment_id")
    
    assessment = await crud_assessment.get(db, assessment_uuid)
    if not assessment:
        raise NotFoundError("Assessment not found")
    
    updated_assessment = await crud_assessment.update(db, assessment, assessment_update)
    
    return {
        "success": True,
        "data": updated_assessment,
        "message": "Assessment updated successfully"
    }


@router.delete("/{assessment_id}")
async def delete_assessment(
    assessment_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_instructor_or_admin)
) -> Dict[str, Any]:
    """Delete assessment by ID (instructors and admins only)."""
    
    assessment_uuid = validate_uuid(assessment_id, "assessment_id")
    
    success = await crud_assessment.delete(db, assessment_uuid)
    if not success:
        raise NotFoundError("Assessment not found")
    
    return {
        "success": True,
        "message": "Assessment deleted successfully"
    }


@router.get("/user/{user_id}", response_model=ApiResponse[List[FitnessAssessment]])
async def get_user_assessments(
    user_id: str,
    assessment_type: AssessmentType = Query(None),
    pagination: PaginationParams = Depends(get_pagination),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get assessments for a specific user."""
    
    user_uuid = validate_uuid(user_id, "user_id")
    
    # Students can only access their own assessments
    if current_user.role == "student" and user_uuid != current_user.id:
        raise NotFoundError("User not found")
    
    if assessment_type:
        assessments = await crud_assessment.get_by_type_and_user(
            db, user_uuid, assessment_type, pagination.offset, pagination.limit
        )
    else:
        assessments = await crud_assessment.get_by_user(
            db, user_uuid, pagination.offset, pagination.limit
        )
    
    return {
        "success": True,
        "data": assessments,
        "message": f"Retrieved {len(assessments)} assessments for user"
    }


@router.get("/pending/list", response_model=ApiResponse[List[FitnessAssessment]])
async def get_pending_assessments(
    pagination: PaginationParams = Depends(get_pagination),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_instructor_or_admin)
) -> Dict[str, Any]:
    """Get pending assessments for processing (instructors and admins only)."""
    
    assessments = await crud_assessment.get_pending_assessments(
        db, pagination.offset, pagination.limit
    )
    
    return {
        "success": True,
        "data": assessments,
        "message": f"Retrieved {len(assessments)} pending assessments"
    }


@router.post("/{assessment_id}/upload-video")
async def upload_assessment_video(
    assessment_id: str,
    video: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Upload video for an assessment."""
    
    assessment_uuid = validate_uuid(assessment_id, "assessment_id")
    
    assessment = await crud_assessment.get(db, assessment_uuid)
    if not assessment:
        raise NotFoundError("Assessment not found")
    
    # Students can only upload to their own assessments
    if current_user.role == "student" and assessment.user_id != current_user.id:
        raise NotFoundError("Assessment not found")
    
    # Validate video file
    if not video.content_type.startswith("video/"):
        raise ValidationError("File must be a video")
    
    # TODO: Implement video upload to S3/MinIO
    # For now, return a mock response
    
    # Update assessment with video URL (mock)
    video_url = f"https://storage.example.com/videos/{assessment_id}/{video.filename}"
    await crud_assessment.update(db, assessment, {
        "video_url": video_url,
        "status": AssessmentStatus.PROCESSING
    })
    
    return {
        "success": True,
        "data": {"video_url": video_url},
        "message": "Video uploaded successfully"
    }


@router.get("/stats/summary")
async def get_assessment_stats(
    user_id: str = Query(None),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get assessment statistics."""
    
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
    
    # Get counts by status
    total_assessments = await crud_assessment.count(db, filter_dict)
    
    pending_count = await crud_assessment.count(db, {**filter_dict, "status": "pending"})
    processing_count = await crud_assessment.count(db, {**filter_dict, "status": "processing"})
    completed_count = await crud_assessment.count(db, {**filter_dict, "status": "completed"})
    failed_count = await crud_assessment.count(db, {**filter_dict, "status": "failed"})
    
    # Get counts by type
    pushup_count = await crud_assessment.count(db, {**filter_dict, "assessment_type": "pushup"})
    situp_count = await crud_assessment.count(db, {**filter_dict, "assessment_type": "situp"})
    running_count = await crud_assessment.count(db, {**filter_dict, "assessment_type": "running"})
    flexibility_count = await crud_assessment.count(db, {**filter_dict, "assessment_type": "flexibility"})
    
    stats = {
        "total_assessments": total_assessments,
        "by_status": {
            "pending": pending_count,
            "processing": processing_count,
            "completed": completed_count,
            "failed": failed_count,
        },
        "by_type": {
            "pushup": pushup_count,
            "situp": situp_count,
            "running": running_count,
            "flexibility": flexibility_count,
        }
    }
    
    return {
        "success": True,
        "data": stats,
        "message": "Assessment statistics retrieved successfully"
    }