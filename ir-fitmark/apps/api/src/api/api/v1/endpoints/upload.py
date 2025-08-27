"""File upload endpoints."""

from typing import Any, Dict, List
from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_db, file_upload as crud_file
from pyshared import (
    ApiResponse,
    UPLOAD_LIMITS,
    generate_secure_filename,
    validate_file_type,
    settings,
)

from ...core.deps import get_current_active_user
from ...core.exceptions import ValidationError

router = APIRouter()


@router.post("/video", response_model=ApiResponse[Dict[str, Any]])
async def upload_video(
    file: UploadFile = File(...),
    purpose: str = "assessment",
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Upload a video file."""
    
    # Validate file type
    if not validate_file_type(file.filename, settings.app.allowed_video_types):
        raise ValidationError("Invalid file type. Only video files are allowed.")
    
    # Validate file size
    if file.size > UPLOAD_LIMITS["MAX_FILE_SIZE"]:
        raise ValidationError(f"File too large. Maximum size is {UPLOAD_LIMITS['MAX_FILE_SIZE'] // (1024*1024)}MB")
    
    # Generate secure filename
    secure_filename = generate_secure_filename(file.filename)
    file_path = f"videos/{current_user.id}/{secure_filename}"
    
    # TODO: Implement actual file upload to S3/MinIO
    # For now, create a mock file upload record
    
    # Calculate file hash (mock)
    file_hash = f"mock_hash_{uuid4().hex[:16]}"
    
    # Create file upload record
    file_upload_data = {
        "user_id": current_user.id,
        "original_filename": file.filename,
        "stored_filename": secure_filename,
        "file_path": file_path,
        "file_size": file.size,
        "mime_type": file.content_type,
        "file_hash": file_hash,
        "upload_type": "video",
        "purpose": purpose,
        "s3_bucket": settings.s3.s3_bucket,
        "s3_key": file_path,
    }
    
    file_record = await crud_file.create(db, file_upload_data)
    
    # Mock S3 URL
    file_url = f"https://{settings.s3.s3_bucket}.s3.{settings.s3.s3_region}.amazonaws.com/{file_path}"
    
    return {
        "success": True,
        "data": {
            "file_id": str(file_record.id),
            "filename": secure_filename,
            "original_filename": file.filename,
            "file_url": file_url,
            "file_size": file.size,
            "mime_type": file.content_type,
            "upload_type": "video",
            "purpose": purpose,
        },
        "message": "Video uploaded successfully"
    }


@router.post("/image", response_model=ApiResponse[Dict[str, Any]])
async def upload_image(
    file: UploadFile = File(...),
    purpose: str = "profile",
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Upload an image file."""
    
    # Validate file type
    if not validate_file_type(file.filename, settings.app.allowed_image_types):
        raise ValidationError("Invalid file type. Only image files are allowed.")
    
    # Validate file size (smaller limit for images)
    max_image_size = 10 * 1024 * 1024  # 10MB
    if file.size > max_image_size:
        raise ValidationError(f"File too large. Maximum size is {max_image_size // (1024*1024)}MB")
    
    # Generate secure filename
    secure_filename = generate_secure_filename(file.filename)
    file_path = f"images/{current_user.id}/{secure_filename}"
    
    # TODO: Implement actual file upload to S3/MinIO
    # For now, create a mock file upload record
    
    # Calculate file hash (mock)
    file_hash = f"mock_hash_{uuid4().hex[:16]}"
    
    # Create file upload record
    file_upload_data = {
        "user_id": current_user.id,
        "original_filename": file.filename,
        "stored_filename": secure_filename,
        "file_path": file_path,
        "file_size": file.size,
        "mime_type": file.content_type,
        "file_hash": file_hash,
        "upload_type": "image",
        "purpose": purpose,
        "s3_bucket": settings.s3.s3_bucket,
        "s3_key": file_path,
    }
    
    file_record = await crud_file.create(db, file_upload_data)
    
    # Mock S3 URL
    file_url = f"https://{settings.s3.s3_bucket}.s3.{settings.s3.s3_region}.amazonaws.com/{file_path}"
    
    return {
        "success": True,
        "data": {
            "file_id": str(file_record.id),
            "filename": secure_filename,
            "original_filename": file.filename,
            "file_url": file_url,
            "file_size": file.size,
            "mime_type": file.content_type,
            "upload_type": "image",
            "purpose": purpose,
        },
        "message": "Image uploaded successfully"
    }


@router.post("/multiple", response_model=ApiResponse[List[Dict[str, Any]]])
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    purpose: str = "assessment",
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Upload multiple files."""
    
    if len(files) > 10:
        raise ValidationError("Cannot upload more than 10 files at once")
    
    uploaded_files = []
    total_size = sum(file.size for file in files)
    
    if total_size > UPLOAD_LIMITS["MAX_FILE_SIZE"] * 2:  # Double limit for multiple files
        raise ValidationError("Total file size too large")
    
    for file in files:
        # Determine file type
        if file.content_type.startswith("video/"):
            if not validate_file_type(file.filename, settings.app.allowed_video_types):
                continue  # Skip invalid files
            upload_type = "video"
            file_path = f"videos/{current_user.id}/{generate_secure_filename(file.filename)}"
        elif file.content_type.startswith("image/"):
            if not validate_file_type(file.filename, settings.app.allowed_image_types):
                continue  # Skip invalid files
            upload_type = "image"
            file_path = f"images/{current_user.id}/{generate_secure_filename(file.filename)}"
        else:
            continue  # Skip unsupported file types
        
        # Generate secure filename
        secure_filename = generate_secure_filename(file.filename)
        
        # Calculate file hash (mock)
        file_hash = f"mock_hash_{uuid4().hex[:16]}"
        
        # Create file upload record
        file_upload_data = {
            "user_id": current_user.id,
            "original_filename": file.filename,
            "stored_filename": secure_filename,
            "file_path": file_path,
            "file_size": file.size,
            "mime_type": file.content_type,
            "file_hash": file_hash,
            "upload_type": upload_type,
            "purpose": purpose,
            "s3_bucket": settings.s3.s3_bucket,
            "s3_key": file_path,
        }
        
        file_record = await crud_file.create(db, file_upload_data)
        
        # Mock S3 URL
        file_url = f"https://{settings.s3.s3_bucket}.s3.{settings.s3.s3_region}.amazonaws.com/{file_path}"
        
        uploaded_files.append({
            "file_id": str(file_record.id),
            "filename": secure_filename,
            "original_filename": file.filename,
            "file_url": file_url,
            "file_size": file.size,
            "mime_type": file.content_type,
            "upload_type": upload_type,
            "purpose": purpose,
        })
    
    return {
        "success": True,
        "data": uploaded_files,
        "message": f"Uploaded {len(uploaded_files)} files successfully"
    }


@router.get("/files")
async def get_user_files(
    upload_type: str = None,
    purpose: str = None,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get user's uploaded files."""
    
    # Build filter conditions
    filter_dict = {"user_id": current_user.id}
    
    if upload_type:
        filter_dict["upload_type"] = upload_type
    
    if purpose:
        filter_dict["purpose"] = purpose
    
    files = await crud_file.get_multi(db, 0, 100, filter_dict)
    
    file_data = []
    for file_record in files:
        file_url = f"https://{file_record.s3_bucket}.s3.{settings.s3.s3_region}.amazonaws.com/{file_record.s3_key}"
        
        file_data.append({
            "file_id": str(file_record.id),
            "filename": file_record.stored_filename,
            "original_filename": file_record.original_filename,
            "file_url": file_url,
            "file_size": file_record.file_size,
            "mime_type": file_record.mime_type,
            "upload_type": file_record.upload_type,
            "purpose": file_record.purpose,
            "uploaded_at": file_record.created_at.isoformat(),
            "is_processed": file_record.is_processed,
        })
    
    return {
        "success": True,
        "data": file_data,
        "message": f"Retrieved {len(file_data)} files"
    }


@router.delete("/files/{file_id}")
async def delete_file(
    file_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Delete an uploaded file."""
    
    from uuid import UUID
    try:
        file_uuid = UUID(file_id)
    except ValueError:
        raise ValidationError("Invalid file ID format")
    
    # Get file record
    file_record = await crud_file.get(db, file_uuid)
    if not file_record:
        raise ValidationError("File not found")
    
    # Check ownership
    if file_record.user_id != current_user.id:
        raise ValidationError("Access denied")
    
    # TODO: Delete file from S3/MinIO
    
    # Delete database record
    await crud_file.delete(db, file_uuid)
    
    return {
        "success": True,
        "message": "File deleted successfully"
    }