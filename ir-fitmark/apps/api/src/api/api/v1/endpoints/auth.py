"""Authentication endpoints."""

from datetime import timedelta
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_db, user as crud_user
from pyshared import (
    ApiResponse,
    Token,
    User,
    UserCreate,
    create_access_token,
    create_refresh_token,
    hash_password,
    settings,
    verify_password,
    verify_token,
)

from ...core.deps import get_current_active_user
from ...core.exceptions import AuthenticationError, ConflictError

router = APIRouter()


@router.post("/register", response_model=ApiResponse[User])
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_async_db)
) -> Dict[str, Any]:
    """Register a new user."""
    
    # Check if user already exists
    existing_user = await crud_user.get_by_email(db, user_data.email)
    if existing_user:
        raise ConflictError("User with this email already exists")
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    
    # Create user
    user_dict = user_data.model_dump()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    
    user = await crud_user.create(db, user_dict)
    
    return {
        "success": True,
        "data": user,
        "message": "User registered successfully"
    }


@router.post("/login", response_model=ApiResponse[Token])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
) -> Dict[str, Any]:
    """Authenticate user and return access token."""
    
    # Get user by email
    user = await crud_user.get_by_email(db, form_data.username)
    if not user:
        raise AuthenticationError("Incorrect email or password")
    
    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise AuthenticationError("Incorrect email or password")
    
    # Check if user is active
    if not user.is_active:
        raise AuthenticationError("User account is disabled")
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.auth.access_token_expire_minutes)
    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        role=user.role,
        expires_delta=access_token_expires
    )
    
    # Create refresh token
    refresh_token = create_refresh_token(user.id)
    
    token_data = Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.auth.access_token_expire_minutes * 60
    )
    
    return {
        "success": True,
        "data": token_data,
        "message": "Login successful"
    }


@router.post("/refresh", response_model=ApiResponse[Token])
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_async_db)
) -> Dict[str, Any]:
    """Refresh access token using refresh token."""
    
    # Verify refresh token
    token_data = verify_token(refresh_token, "refresh")
    if not token_data or not token_data.user_id:
        raise AuthenticationError("Invalid refresh token")
    
    # Get user
    user = await crud_user.get(db, token_data.user_id)
    if not user or not user.is_active:
        raise AuthenticationError("User not found or disabled")
    
    # Create new access token
    access_token_expires = timedelta(minutes=settings.auth.access_token_expire_minutes)
    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        role=user.role,
        expires_delta=access_token_expires
    )
    
    token_data = Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.auth.access_token_expire_minutes * 60
    )
    
    return {
        "success": True,
        "data": token_data,
        "message": "Token refreshed successfully"
    }


@router.get("/profile", response_model=ApiResponse[User])
async def get_profile(
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get current user profile."""
    
    return {
        "success": True,
        "data": current_user,
        "message": "Profile retrieved successfully"
    }


@router.put("/profile", response_model=ApiResponse[User])
async def update_profile(
    user_update: UserUpdate,
    current_user = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
) -> Dict[str, Any]:
    """Update current user profile."""
    
    # Update user
    updated_user = await crud_user.update(db, current_user, user_update)
    
    return {
        "success": True,
        "data": updated_user,
        "message": "Profile updated successfully"
    }


@router.post("/logout")
async def logout(
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Logout user (client should discard token)."""
    
    return {
        "success": True,
        "message": "Logout successful"
    }


@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
) -> Dict[str, Any]:
    """Change user password."""
    
    # Verify current password
    if not verify_password(current_password, current_user.hashed_password):
        raise AuthenticationError("Current password is incorrect")
    
    # Hash new password
    hashed_password = hash_password(new_password)
    
    # Update password
    await crud_user.update(db, current_user, {"hashed_password": hashed_password})
    
    return {
        "success": True,
        "message": "Password changed successfully"
    }