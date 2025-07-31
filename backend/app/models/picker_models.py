# File: backend/app/models/picker_models.py
# Path: backend/app/models/picker_models.py

"""
Picker models for the logistics management system.
"""

from typing import Optional
from pydantic import BaseModel, Field


class Picker(BaseModel):
    """Model for warehouse picker."""

    picker_id: str = Field(..., description="Unique picker ID")
    name: str = Field(..., description="Picker name")
    employee_number: str = Field(..., description="Employee number")
    is_active: bool = Field(default=True, description="Active status")
    current_order: Optional[str] = Field(None, description="Current order ID")
    total_picks_today: int = Field(default=0, ge=0, description="Total picks today")
    efficiency_rating: float = Field(
        default=1.0, ge=0.0, le=2.0, description="Efficiency rating"
    )


class PickerCreate(BaseModel):
    """Model for creating a new picker."""

    name: str = Field(..., description="Picker name")
    employee_number: str = Field(..., description="Employee number")


class PickerResponse(BaseModel):
    """Picker response model."""

    picker_id: str = Field(..., description="Picker ID")
    name: str = Field(..., description="Picker name")
    employee_number: str = Field(..., description="Employee number")
    is_active: bool = Field(..., description="Active status")
    current_order: Optional[str] = Field(None, description="Current order ID")
    total_picks_today: int = Field(..., description="Total picks today")
    efficiency_rating: float = Field(..., description="Efficiency rating")


# EOF
