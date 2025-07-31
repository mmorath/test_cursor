# File: backend/app/models/cart_models.py
# Path: backend/app/models/cart_models.py

"""
Cart models for the logistics management system.
"""

from typing import Optional
from pydantic import BaseModel, Field


class MaterialCart(BaseModel):
    """Model for material cart."""
    cart_id: str = Field(..., description="Unique cart ID")
    assigned_picker: Optional[str] = Field(None, description="Assigned picker")
    current_order: Optional[str] = Field(None, description="Current order ID")
    capacity: float = Field(..., ge=0, description="Weight capacity")
    current_weight: float = Field(default=0.0, ge=0, description="Current weight")
    is_available: bool = Field(default=True, description="Availability status")

    @property
    def available_capacity(self) -> float:
        """Calculate available capacity."""
        return max(0, self.capacity - self.current_weight)

    @property
    def utilization_percentage(self) -> float:
        """Calculate utilization percentage."""
        if self.capacity == 0:
            return 0.0
        return (self.current_weight / self.capacity) * 100


class CartCreate(BaseModel):
    """Model for creating a new cart."""
    capacity: float = Field(..., ge=0, description="Weight capacity")


class CartResponse(BaseModel):
    """Cart response model."""
    cart_id: str = Field(..., description="Cart ID")
    assigned_picker: Optional[str] = Field(None, description="Assigned picker")
    current_order: Optional[str] = Field(None, description="Current order ID")
    capacity: float = Field(..., description="Weight capacity")
    current_weight: float = Field(..., description="Current weight")
    available_capacity: float = Field(..., description="Available capacity")
    utilization_percentage: float = Field(..., description="Utilization percentage")
    is_available: bool = Field(..., description="Availability status")


# EOF