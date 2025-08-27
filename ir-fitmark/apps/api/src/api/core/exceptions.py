"""Exception handlers for the FastAPI application."""

from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


class IRFitMarkException(Exception):
    """Base exception for IR FitMark application."""
    
    def __init__(self, message: str, code: str = None, status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(IRFitMarkException):
    """Exception raised when a resource is not found."""
    
    def __init__(self, message: str = "Resource not found", code: str = "NOT_FOUND"):
        super().__init__(message, code, 404)


class AuthenticationError(IRFitMarkException):
    """Exception raised for authentication failures."""
    
    def __init__(self, message: str = "Authentication failed", code: str = "AUTH_FAILED"):
        super().__init__(message, code, 401)


class AuthorizationError(IRFitMarkException):
    """Exception raised for authorization failures."""
    
    def __init__(self, message: str = "Access denied", code: str = "ACCESS_DENIED"):
        super().__init__(message, code, 403)


class ValidationError(IRFitMarkException):
    """Exception raised for validation failures."""
    
    def __init__(self, message: str = "Validation failed", code: str = "VALIDATION_ERROR"):
        super().__init__(message, code, 422)


class ConflictError(IRFitMarkException):
    """Exception raised for resource conflicts."""
    
    def __init__(self, message: str = "Resource conflict", code: str = "CONFLICT"):
        super().__init__(message, code, 409)


class RateLimitError(IRFitMarkException):
    """Exception raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", code: str = "RATE_LIMIT"):
        super().__init__(message, code, 429)


def create_error_response(
    status_code: int,
    message: str,
    code: str = None,
    details: Any = None,
    request_id: str = None
) -> Dict[str, Any]:
    """Create a standardized error response."""
    response = {
        "success": False,
        "error": message,
        "code": code,
    }
    
    if details:
        response["details"] = details
    
    if request_id:
        response["request_id"] = request_id
    
    return response


async def ir_fitmark_exception_handler(request: Request, exc: IRFitMarkException) -> JSONResponse:
    """Handle custom IR FitMark exceptions."""
    request_id = getattr(request.state, "request_id", None)
    
    logger.warning(
        f"IR FitMark exception: {exc.message}",
        extra={
            "request_id": request_id,
            "exception_type": type(exc).__name__,
            "status_code": exc.status_code,
            "code": exc.code,
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            status_code=exc.status_code,
            message=exc.message,
            code=exc.code,
            request_id=request_id,
        )
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTP exceptions."""
    request_id = getattr(request.state, "request_id", None)
    
    logger.warning(
        f"HTTP exception: {exc.detail}",
        extra={
            "request_id": request_id,
            "status_code": exc.status_code,
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            status_code=exc.status_code,
            message=exc.detail,
            request_id=request_id,
        )
    )


async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle Pydantic validation exceptions."""
    request_id = getattr(request.state, "request_id", None)
    
    logger.warning(
        f"Validation exception",
        extra={
            "request_id": request_id,
            "errors": exc.errors(),
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=create_error_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Validation error",
            code="VALIDATION_ERROR",
            details=exc.errors(),
            request_id=request_id,
        )
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """Handle SQLAlchemy integrity errors."""
    request_id = getattr(request.state, "request_id", None)
    
    logger.error(
        f"Database integrity error",
        extra={
            "request_id": request_id,
            "error": str(exc.orig),
        }
    )
    
    # Parse common integrity errors
    error_message = "Database constraint violation"
    if "unique" in str(exc.orig).lower():
        error_message = "Resource already exists"
    elif "foreign key" in str(exc.orig).lower():
        error_message = "Referenced resource not found"
    elif "not null" in str(exc.orig).lower():
        error_message = "Required field missing"
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=create_error_response(
            status_code=status.HTTP_409_CONFLICT,
            message=error_message,
            code="INTEGRITY_ERROR",
            request_id=request_id,
        )
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions."""
    request_id = getattr(request.state, "request_id", None)
    
    logger.exception(
        f"Unhandled exception",
        extra={
            "request_id": request_id,
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=create_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            code="INTERNAL_ERROR",
            request_id=request_id,
        )
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Set up exception handlers for the FastAPI application."""
    
    # Custom exception handlers
    app.add_exception_handler(IRFitMarkException, ir_fitmark_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)