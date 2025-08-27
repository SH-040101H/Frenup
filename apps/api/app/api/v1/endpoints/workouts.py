"""Workout endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import get_current_user
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/")
async def get_workouts(current_user: UserResponse = Depends(get_current_user)):
    """Get all workouts."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented yet",
    )