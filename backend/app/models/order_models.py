# File: backend/app/models/order_models.py
# Path: backend/app/models/order_models.py

"""
Order models for the logistics management system.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .project_models import Project
from .common_models import StatusEnum


class PickingOrder(BaseModel):
    """Model for a picking order."""
    order_id: str = Field(..., description="Unique order ID")
    project: Project = Field(..., description="Associated project")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation time")
    assigned_picker: Optional[str] = Field(None, description="Assigned picker")
    status: StatusEnum = Field(default=StatusEnum.OFFEN, description="Order status")
    priority: int = Field(default=1, ge=1, le=10, description="Priority level")
    estimated_duration: Optional[int] = Field(None, ge=0, description="Estimated duration in minutes")

    @property
    def is_complete(self) -> bool:
        """Check if all articles are completed."""
        return all(article.status == StatusEnum.ABGESCHLOSSEN
                  for article in self.project.articles)

    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage."""
        if not self.project.articles:
            return 0.0
        completed = len(self.project.completed_articles)
        total = len(self.project.articles)
        return (completed / total) * 100


class OrderCreate(BaseModel):
    """Model for creating a new order."""
    project_number: str = Field(..., description="Project number")
    priority: int = Field(default=1, ge=1, le=10, description="Priority level")


class OrderResponse(BaseModel):
    """Order response model."""
    order_id: str = Field(..., description="Order ID")
    project_number: str = Field(..., description="Project number")
    status: StatusEnum = Field(..., description="Order status")
    priority: int = Field(..., description="Priority level")
    assigned_picker: Optional[str] = Field(None, description="Assigned picker")
    created_at: datetime = Field(..., description="Creation time")
    completion_percentage: float = Field(..., description="Completion percentage")
    total_articles: int = Field(..., description="Total articles")
    completed_articles: int = Field(..., description="Completed articles")
    total_weight: float = Field(..., description="Total weight")
    is_complete: bool = Field(..., description="Completion status")


class OrderList(BaseModel):
    """Order list response model."""
    orders: List[OrderResponse] = Field(..., description="List of orders")
    total: int = Field(..., description="Total orders")
    page: int = Field(..., description="Current page")
    size: int = Field(..., description="Page size")


# EOF