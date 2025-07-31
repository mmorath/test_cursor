# File: backend/app/models/project_models.py
# Path: backend/app/models/project_models.py

"""
Project models for the logistics management system.
"""

from typing import List
from pydantic import BaseModel, Field
from .article_models import Article
from .common_models import StatusEnum


class Project(BaseModel):
    """Model for a project containing multiple articles."""

    projekt_nr: str = Field(..., description="Project number")
    articles: List[Article] = Field(default_factory=list, description="Articles")

    @property
    def total_articles(self) -> int:
        """Get total number of articles in project."""
        return len(self.articles)

    @property
    def total_weight(self) -> float:
        """Calculate total weight of all articles."""
        return sum(article.total_weight for article in self.articles)

    @property
    def open_articles(self) -> List[Article]:
        """Get articles with open status."""
        return [
            article for article in self.articles if article.status == StatusEnum.OFFEN
        ]

    @property
    def completed_articles(self) -> List[Article]:
        """Get articles with completed status."""
        return [
            article
            for article in self.articles
            if article.status == StatusEnum.ABGESCHLOSSEN
        ]


class ProjectCreate(BaseModel):
    """Model for creating a new project."""

    projekt_nr: str = Field(..., description="Project number")


class ProjectResponse(BaseModel):
    """Project response model."""

    projekt_nr: str = Field(..., description="Project number")
    total_articles: int = Field(..., description="Total articles")
    total_weight: float = Field(..., description="Total weight")
    open_articles: int = Field(..., description="Open articles count")
    completed_articles: int = Field(..., description="Completed articles count")
    completion_percentage: float = Field(..., description="Completion percentage")

    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage."""
        if self.total_articles == 0:
            return 0.0
        return (self.completed_articles / self.total_articles) * 100


# EOF
