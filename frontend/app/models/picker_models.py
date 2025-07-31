# File: frontend/app/models/picker_models.py
# Path: frontend/app/models/picker_models.py

"""
Picker models for UI validation and configuration.
"""

from typing import Optional
from pydantic import BaseModel, Field


class PickerCreate(BaseModel):
    """Model for creating a new picker."""
    name: str = Field(..., description="Picker name")
    employee_number: str = Field(..., description="Employee number")


class PickerUpdate(BaseModel):
    """Model for updating a picker."""
    name: Optional[str] = Field(None, description="Picker name")
    employee_number: Optional[str] = Field(None, description="Employee number")
    is_active: Optional[bool] = Field(None, description="Active status")


# EOF