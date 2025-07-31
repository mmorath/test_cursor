# File: frontend/app/models/cart_models.py
# Path: frontend/app/models/cart_models.py

"""
Cart models for UI validation and configuration.
"""

from typing import Optional
from pydantic import BaseModel, Field


class CartCreate(BaseModel):
    """Model for creating a new cart."""
    capacity: float = Field(..., ge=0, description="Weight capacity")


class CartUpdate(BaseModel):
    """Model for updating a cart."""
    capacity: Optional[float] = Field(None, ge=0, description="Weight capacity")
    is_available: Optional[bool] = Field(None, description="Availability status")


# EOF