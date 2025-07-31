# File: frontend/app/models/order_models.py
# Path: frontend/app/models/order_models.py

"""
Order models for UI validation and configuration.
"""

from typing import Optional
from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    """Model for creating a new order."""

    project_number: str = Field(..., description="Project number")
    priority: int = Field(1, ge=1, le=10, description="Priority level")


class OrderFilter(BaseModel):
    """Model for filtering orders."""

    status: Optional[str] = Field(None, description="Filter by status")
    assigned_picker: Optional[str] = Field(None, description="Filter by picker")
    priority: Optional[int] = Field(None, ge=1, le=10, description="Filter by priority")


# EOF
