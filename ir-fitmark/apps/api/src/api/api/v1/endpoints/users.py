"""User management endpoints."""

from typing import Any, Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_db, user as crud_user
from pyshared import ApiResponse, PaginatedResponse, User, UserUpdate

from ...core.deps import (
    get_current_active_user,
    get_pagination,
    get_filter_params,
    require_admin,
    require_instructor_or_admin,
    validate_uuid,
    PaginationParams,
    FilterParams,
)
from ...core.exceptions import NotFoundError

router = APIRouter()


@router.get("/", response_model=ApiResponse[PaginatedResponse[User]])
async def get_users(
    pagination: PaginationParams = Depends(get_pagination),
    filters: FilterParams = Depends(get_filter_params),
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_instructor_or_admin)
) -> Dict[str, Any]:
    """Get paginated list of users (instructors and admins only)."""
    
    # Build filter conditions
    filter_dict = {}
    if filters.status:
        filter_dict["is_active"] = filters.status.lower() == "active"
    
    # Get users
    if filters.search:
        users = await crud_user.search_users(
            db, filters.search, pagination.offset, pagination.limit
        )
        total = await crud_user.count(db, filter_dict)
    else:
        users = await crud_user.get_multi(
            db, pagination.offset, pagination.limit, filter_dict
        )
        total = await crud_user.count(db, filter_dict)
    
    # Create paginated response
    paginated_data = {
        "items": users,
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
        "message": f"Retrieved {len(users)} users"
    }


@router.get("/{user_id}", response_model=ApiResponse[User])
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_instructor_or_admin)
) -> Dict[str, Any]:
    """Get user by ID (instructors and admins only)."""
    
    user_uuid = validate_uuid(user_id, "user_id")
    
    user = await crud_user.get(db, user_uuid)
    if not user:
        raise NotFoundError("User not found")
    
    return {
        "success": True,
        "data": user,
        "message": "User retrieved successfully"
    }


@router.put("/{user_id}", response_model=ApiResponse[User])
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_admin)
) -> Dict[str, Any]:
    """Update user by ID (admins only)."""
    
    user_uuid = validate_uuid(user_id, "user_id")
    
    user = await crud_user.get(db, user_uuid)
    if not user:
        raise NotFoundError("User not found")
    
    updated_user = await crud_user.update(db, user, user_update)
    
    return {
        "success": True,
        "data": updated_user,
        "message": "User updated successfully"
    }


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_admin)
) -> Dict[str, Any]:
    """Delete user by ID (admins only)."""
    
    user_uuid = validate_uuid(user_id, "user_id")
    
    # Check if user exists
    user = await crud_user.get(db, user_uuid)
    if not user:
        raise NotFoundError("User not found")
    
    # Soft delete by deactivating
    await crud_user.update(db, user, {"is_active": False})
    
    return {
        "success": True,
        "message": "User deleted successfully"
    }


@router.get("/active/count")
async def get_active_users_count(
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_instructor_or_admin)
) -> Dict[str, Any]:
    """Get count of active users."""
    
    count = await crud_user.count(db, {"is_active": True})
    
    return {
        "success": True,
        "data": {"count": count},
        "message": f"Found {count} active users"
    }


@router.get("/stats/summary")
async def get_user_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(require_admin)
) -> Dict[str, Any]:
    """Get user statistics summary (admins only)."""
    
    total_users = await crud_user.count(db)
    active_users = await crud_user.count(db, {"is_active": True})
    inactive_users = total_users - active_users
    
    # Count by role
    admin_count = await crud_user.count(db, {"role": "admin"})
    instructor_count = await crud_user.count(db, {"role": "instructor"})
    student_count = await crud_user.count(db, {"role": "student"})
    
    stats = {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "by_role": {
            "admin": admin_count,
            "instructor": instructor_count,
            "student": student_count,
        }
    }
    
    return {
        "success": True,
        "data": stats,
        "message": "User statistics retrieved successfully"
    }