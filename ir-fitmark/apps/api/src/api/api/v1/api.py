"""API v1 router configuration."""

from fastapi import APIRouter

from .endpoints import (
    auth,
    users,
    assessments,
    reports,
    qr,
    admin,
    upload,
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(qr.router, prefix="/qr", tags=["qr-codes"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])