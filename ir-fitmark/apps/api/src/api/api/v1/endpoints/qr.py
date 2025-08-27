"""QR code management endpoints."""

from typing import Any, Dict, List
from uuid import UUID
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_db, qr_code as crud_qr
from pyshared import (
    ApiResponse,
    PaginatedResponse,
    QRCode,
    QRCodeCreate,
    generate_qr_code,
)

from ...core.deps import (
    get_current_active_user,
    get_pagination,
    require_instructor_or_admin,
    require_admin,
    validate_uuid,
    PaginationParams,
)
from ...core.exceptions import NotFoundError, ValidationError

router = APIRouter()


@router.post("/generate", response_model=ApiResponse[QRCode])
async def generate_qr_code_endpoint(
    user_id: str,
    expires_in_hours: int = Query(24, ge=1, le=168),  # 1 hour to 1 week
    max_usage: int = Query(1, ge=1, le=100),
    qr_type: str = Query("assessment"),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_instructor_or_admin)
) -> Dict[str, Any]:
    """Generate a new QR code for a user."""
    
    user_uuid = validate_uuid(user_id, "user_id")
    
    # Generate unique QR code
    code = generate_qr_code()
    expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
    
    qr_create = QRCodeCreate(
        code=code,
        user_id=user_uuid,
        expires_at=expires_at,
        max_usage=max_usage,
        qr_type=qr_type,
        metadata={
            "generated_by": str(current_user.id),
            "generated_at": datetime.utcnow().isoformat(),
            "type": qr_type,
        }
    )
    
    qr_code = await crud_qr.create(db, qr_create)
    
    return {
        "success": True,
        "data": qr_code,
        "message": "QR code generated successfully"
    }


@router.post("/bulk-generate")
async def bulk_generate_qr_codes(
    user_ids: List[str],
    expires_in_hours: int = Query(24, ge=1, le=168),
    max_usage: int = Query(1, ge=1, le=100),
    qr_type: str = Query("assessment"),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_admin)
) -> Dict[str, Any]:
    """Bulk generate QR codes for multiple users (admins only)."""
    
    if len(user_ids) > 100:
        raise ValidationError("Cannot generate more than 100 QR codes at once")
    
    generated_codes = []
    expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
    
    for user_id in user_ids:
        user_uuid = validate_uuid(user_id, "user_id")
        
        # Generate unique QR code
        code = generate_qr_code()
        
        qr_create = QRCodeCreate(
            code=code,
            user_id=user_uuid,
            expires_at=expires_at,
            max_usage=max_usage,
            qr_type=qr_type,
            metadata={
                "generated_by": str(current_user.id),
                "generated_at": datetime.utcnow().isoformat(),
                "type": qr_type,
                "bulk_generation": True,
            }
        )
        
        qr_code = await crud_qr.create(db, qr_create)
        generated_codes.append(qr_code)
    
    return {
        "success": True,
        "data": {
            "generated_count": len(generated_codes),
            "qr_codes": generated_codes
        },
        "message": f"Generated {len(generated_codes)} QR codes successfully"
    }


@router.post("/verify")
async def verify_qr_code(
    code: str,
    db: AsyncSession = Depends(get_async_db)
) -> Dict[str, Any]:
    """Verify a QR code and return user information."""
    
    qr_code = await crud_qr.get_by_code(db, code)
    if not qr_code:
        raise NotFoundError("Invalid QR code")
    
    # Check if QR code is active
    if not qr_code.is_active:
        return {
            "success": False,
            "error": "QR code is inactive",
            "message": "This QR code has been deactivated"
        }
    
    # Check if QR code has expired
    if qr_code.expires_at < datetime.utcnow():
        return {
            "success": False,
            "error": "QR code expired",
            "message": "This QR code has expired"
        }
    
    # Check usage limit
    if qr_code.usage_count >= qr_code.max_usage:
        return {
            "success": False,
            "error": "QR code usage limit exceeded",
            "message": "This QR code has reached its usage limit"
        }
    
    # Increment usage count
    updated_qr = await crud_qr.increment_usage(db, qr_code)
    
    return {
        "success": True,
        "data": {
            "user_id": str(qr_code.user_id),
            "qr_type": qr_code.qr_type,
            "usage_count": updated_qr.usage_count,
            "max_usage": updated_qr.max_usage,
            "is_active": updated_qr.is_active,
        },
        "message": "QR code verified successfully"
    }


@router.get("/", response_model=ApiResponse[PaginatedResponse[QRCode]])
async def get_qr_codes(
    pagination: PaginationParams = Depends(get_pagination),
    user_id: str = Query(None),
    is_active: bool = Query(None),
    qr_type: str = Query(None),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_instructor_or_admin)
) -> Dict[str, Any]:
    """Get paginated list of QR codes."""
    
    # Build filter conditions
    filter_dict = {}
    
    if user_id:
        filter_dict["user_id"] = validate_uuid(user_id, "user_id")
    
    if is_active is not None:
        filter_dict["is_active"] = is_active
    
    if qr_type:
        filter_dict["qr_type"] = qr_type
    
    # Get QR codes
    qr_codes = await crud_qr.get_multi(
        db, pagination.offset, pagination.limit, filter_dict
    )
    total = await crud_qr.count(db, filter_dict)
    
    # Create paginated response
    paginated_data = {
        "items": qr_codes,
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
        "message": f"Retrieved {len(qr_codes)} QR codes"
    }


@router.get("/{qr_id}", response_model=ApiResponse[QRCode])
async def get_qr_code(
    qr_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_instructor_or_admin)
) -> Dict[str, Any]:
    """Get QR code by ID."""
    
    qr_uuid = validate_uuid(qr_id, "qr_id")
    
    qr_code = await crud_qr.get(db, qr_uuid)
    if not qr_code:
        raise NotFoundError("QR code not found")
    
    return {
        "success": True,
        "data": qr_code,
        "message": "QR code retrieved successfully"
    }


@router.put("/{qr_id}/deactivate")
async def deactivate_qr_code(
    qr_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_instructor_or_admin)
) -> Dict[str, Any]:
    """Deactivate a QR code."""
    
    qr_uuid = validate_uuid(qr_id, "qr_id")
    
    qr_code = await crud_qr.get(db, qr_uuid)
    if not qr_code:
        raise NotFoundError("QR code not found")
    
    updated_qr = await crud_qr.update(db, qr_code, {"is_active": False})
    
    return {
        "success": True,
        "data": updated_qr,
        "message": "QR code deactivated successfully"
    }


@router.delete("/{qr_id}")
async def delete_qr_code(
    qr_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_admin)
) -> Dict[str, Any]:
    """Delete QR code by ID (admins only)."""
    
    qr_uuid = validate_uuid(qr_id, "qr_id")
    
    success = await crud_qr.delete(db, qr_uuid)
    if not success:
        raise NotFoundError("QR code not found")
    
    return {
        "success": True,
        "message": "QR code deleted successfully"
    }


@router.get("/user/{user_id}", response_model=ApiResponse[List[QRCode]])
async def get_user_qr_codes(
    user_id: str,
    is_active: bool = Query(None),
    pagination: PaginationParams = Depends(get_pagination),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_instructor_or_admin)
) -> Dict[str, Any]:
    """Get QR codes for a specific user."""
    
    user_uuid = validate_uuid(user_id, "user_id")
    
    qr_codes = await crud_qr.get_active_codes(
        db, user_uuid, pagination.offset, pagination.limit
    )
    
    # Filter by active status if specified
    if is_active is not None:
        qr_codes = [qr for qr in qr_codes if qr.is_active == is_active]
    
    return {
        "success": True,
        "data": qr_codes,
        "message": f"Retrieved {len(qr_codes)} QR codes for user"
    }


@router.get("/stats/summary")
async def get_qr_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_instructor_or_admin)
) -> Dict[str, Any]:
    """Get QR code statistics."""
    
    total_qr_codes = await crud_qr.count(db)
    active_qr_codes = await crud_qr.count(db, {"is_active": True})
    inactive_qr_codes = total_qr_codes - active_qr_codes
    
    # Count by type
    assessment_count = await crud_qr.count(db, {"qr_type": "assessment"})
    login_count = await crud_qr.count(db, {"qr_type": "login"})
    
    stats = {
        "total_qr_codes": total_qr_codes,
        "active_qr_codes": active_qr_codes,
        "inactive_qr_codes": inactive_qr_codes,
        "by_type": {
            "assessment": assessment_count,
            "login": login_count,
        }
    }
    
    return {
        "success": True,
        "data": stats,
        "message": "QR code statistics retrieved successfully"
    }