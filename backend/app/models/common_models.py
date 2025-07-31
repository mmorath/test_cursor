# File: backend/app/models/common_models.py
# Path: backend/app/models/common_models.py

"""
Common models and enums for the logistics management system.
"""

from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    """Order and article status enumeration."""

    OFFEN = "Offen"
    IN_BEARBEITUNG = "In Bearbeitung"
    ABGESCHLOSSEN = "Abgeschlossen"
    STORNIERT = "Storniert"


class BaseResponse(BaseModel):
    """Standard API response format."""

    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


class ErrorResponse(BaseModel):
    """Standard error response format."""

    status: str = Field("error", description="Error status")
    message: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Error details")
    code: int = Field(..., description="HTTP status code")


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints."""

    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(10, ge=1, le=100, description="Page size")


class PaginationResponse(BaseModel):
    """Pagination response metadata."""

    page: int = Field(..., description="Current page")
    size: int = Field(..., description="Page size")
    total: int = Field(..., description="Total items")
    pages: int = Field(..., description="Total pages")


# EOF
