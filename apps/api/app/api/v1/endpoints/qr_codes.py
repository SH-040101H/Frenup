"""QR code endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import get_current_user
from app.schemas.user import UserResponse

router = APIRouter()


@router.post("/generate")
async def generate_qr_code(current_user: UserResponse = Depends(get_current_user)):
    """Generate a QR code."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented yet",
    )