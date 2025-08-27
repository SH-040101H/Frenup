"""Dependency injection for FastAPI endpoints."""

from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_db, user as crud_user
from pyshared import TokenData, UserRole, verify_token

from .exceptions import AuthenticationError, AuthorizationError

# Security scheme
security = HTTPBearer()


async def get_current_user_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """Get current user from JWT token."""
    if not credentials:
        raise AuthenticationError("Missing authentication token")
    
    token_data = verify_token(credentials.credentials)
    if not token_data:
        raise AuthenticationError("Invalid or expired token")
    
    return token_data


async def get_current_user(
    db: AsyncSession = Depends(get_async_db),
    token_data: TokenData = Depends(get_current_user_token)
):
    """Get current user from database."""
    if not token_data.user_id:
        raise AuthenticationError("Invalid token payload")
    
    user = await crud_user.get(db, token_data.user_id)
    if not user:
        raise AuthenticationError("User not found")
    
    if not user.is_active:
        raise AuthenticationError("User account is disabled")
    
    return user


async def get_current_active_user(
    current_user = Depends(get_current_user)
):
    """Get current active user."""
    if not current_user.is_active:
        raise AuthenticationError("User account is disabled")
    return current_user


def require_roles(allowed_roles: list[UserRole]):
    """Dependency factory for role-based access control."""
    
    def role_checker(current_user = Depends(get_current_active_user)):
        if current_user.role not in allowed_roles:
            raise AuthorizationError(
                f"Access denied. Required roles: {[role.value for role in allowed_roles]}"
            )
        return current_user
    
    return role_checker


# Common role dependencies
require_admin = require_roles([UserRole.ADMIN])
require_instructor_or_admin = require_roles([UserRole.INSTRUCTOR, UserRole.ADMIN])
require_any_authenticated = require_roles([UserRole.STUDENT, UserRole.INSTRUCTOR, UserRole.ADMIN])


def get_optional_current_user(
    db: AsyncSession = Depends(get_async_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
):
    """Get current user if token is provided, otherwise return None."""
    if not credentials:
        return None
    
    try:
        token_data = verify_token(credentials.credentials)
        if not token_data or not token_data.user_id:
            return None
        
        user = crud_user.get(db, token_data.user_id)
        if not user or not user.is_active:
            return None
        
        return user
    except Exception:
        return None


class PaginationParams:
    """Pagination parameters dependency."""
    
    def __init__(self, page: int = 1, limit: int = 10):
        if page < 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Page number must be greater than 0"
            )
        
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Limit must be between 1 and 100"
            )
        
        self.page = page
        self.limit = limit
        self.offset = (page - 1) * limit


def get_pagination(page: int = 1, limit: int = 10) -> PaginationParams:
    """Get pagination parameters."""
    return PaginationParams(page=page, limit=limit)


class FilterParams:
    """Common filter parameters."""
    
    def __init__(
        self,
        search: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        status: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "desc"
    ):
        self.search = search
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.sort_by = sort_by
        self.sort_order = sort_order.lower() if sort_order else "desc"
        
        if self.sort_order not in ["asc", "desc"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="sort_order must be 'asc' or 'desc'"
            )


def get_filter_params(
    search: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "desc"
) -> FilterParams:
    """Get filter parameters."""
    return FilterParams(
        search=search,
        start_date=start_date,
        end_date=end_date,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order
    )


def validate_uuid(uuid_str: str, param_name: str = "id") -> UUID:
    """Validate and convert UUID string."""
    try:
        return UUID(uuid_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid {param_name} format. Must be a valid UUID."
        )