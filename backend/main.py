# File: backend/main.py
# Path: backend/main.py

"""
Main FastAPI application for the logistics management system.
"""

import logging
import logging.config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.models import BaseResponse, ErrorResponse
from config import settings, get_logging_config


# MARK: ━━━ Logging Setup ━━━

logging_config = get_logging_config()
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


# MARK: ━━━ FastAPI Application ━━━

app = FastAPI(
    title=settings.app_name,
    description="Warehouse management and picking system API",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# MARK: ━━━ Global Exception Handler ━━━


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions."""
    logger.error("❌ Unhandled exception: %s", str(exc))

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            status="error",
            message="Internal Server Error",
            details="An unexpected error occurred",
            code=500,
        ).dict(),
    )


# MARK: ━━━ Health Check Endpoints ━━━


@app.get("/")
async def root():
    """Root endpoint."""
    return BaseResponse(
        status="success",
        message=f"{settings.app_name} API is running",
        data={
            "version": settings.app_version,
            "docs": "/docs",
            "health": "/health",
        },
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return BaseResponse(
        status="success",
        message="System is healthy",
        data={"status": "operational"},
    )


# MARK: ━━━ API Routes ━━━

# Include API v1 routes
app.include_router(api_router)


# MARK: ━━━ Startup Event ━━━


@app.on_event("startup")
async def startup_event():
    """Initialize system on startup."""
    logger.info("🚀 Starting %s v%s", settings.app_name, settings.app_version)
    logger.info(
        "📡 Server will be available at http://%s:%s",
        settings.host,
        settings.port,
    )


# MARK: ━━━ Shutdown Event ━━━


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("🛑 Shutting down %s", settings.app_name)


# EOF
