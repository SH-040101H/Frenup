"""Main API router."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, workouts, assessments, files, qr_codes

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(workouts.router, prefix="/workouts", tags=["workouts"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(qr_codes.router, prefix="/qr-codes", tags=["qr-codes"])