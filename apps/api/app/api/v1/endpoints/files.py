"""File upload endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import get_current_user
from app.schemas.user import UserResponse

router = APIRouter()


@router.post("/upload")
async def upload_file(current_user: UserResponse = Depends(get_current_user)):
    """Upload a file."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented yet",
    )