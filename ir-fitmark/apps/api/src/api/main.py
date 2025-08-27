"""Main FastAPI application."""

import time
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from db import close_db, init_db
from pyshared import settings

from .api.v1.api import api_router
from .core.exceptions import setup_exception_handlers
from .core.middleware import (
    LoggingMiddleware,
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for the FastAPI application."""
    # Startup
    logger.info("Starting up IR FitMark API...")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down IR FitMark API...")
    await close_db()
    logger.info("Database connections closed")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title=settings.app.app_name,
        version=settings.app.app_version,
        description="Production-ready FastAPI backend for IR FitMark fitness assessment platform",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        lifespan=lifespan,
    )
    
    # Set up CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.app.cors_origins,
        allow_credentials=settings.app.cors_allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add trusted host middleware for production
    if settings.app.environment == "production":
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"]  # Configure as needed
        )
    
    # Add custom middleware
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(LoggingMiddleware)
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    # Set up exception handlers
    setup_exception_handlers(app)
    
    # Health check endpoint
    @app.get("/health")
    async def health_check() -> Dict[str, Any]:
        """Health check endpoint."""
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "version": settings.app.app_version,
            "environment": settings.app.environment,
        }
    
    # Root endpoint
    @app.get("/")
    async def root() -> Dict[str, str]:
        """Root endpoint."""
        return {
            "message": "Welcome to IR FitMark API",
            "version": settings.app.app_version,
            "docs": "/api/docs",
        }
    
    return app


# Create the application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.app.api_host,
        port=settings.app.api_port,
        reload=settings.app.debug,
        workers=1 if settings.app.debug else settings.app.api_workers,
        access_log=settings.app.debug,
        log_level="debug" if settings.app.debug else "info",
    )