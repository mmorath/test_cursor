# File: backend/app/models/article_models.py
# Path: backend/app/models/article_models.py

"""
Article models for the logistics management system.
"""

from typing import Optional
from pydantic import BaseModel, Field, validator
from .common_models import StatusEnum


class Article(BaseModel):
    """Article model for individual article/order line."""

    projekt_nr: str = Field(..., description="Project number")
    abteilungsgruppe: str = Field(..., description="Department group")
    kostenstelle: str = Field(..., description="Cost center")
    baugruppe: str = Field(..., description="Assembly group")
    artikel: str = Field(..., description="Article number")
    artikel_bezeichnung: str = Field(..., description="Article description")
    menge: int = Field(..., ge=0, description="Quantity")
    einheit: str = Field(..., description="Unit")
    gewicht: float = Field(..., ge=0, description="Weight")
    lagerplatz: str = Field(..., description="Storage location")
    filter: str = Field(..., description="Filter code")
    bestand: int = Field(..., ge=0, description="Current stock")
    wohin: str = Field(..., description="Destination")
    lz: str = Field(default="", description="Lead time")
    lager_1_stueckliste: str = Field(..., description="Warehouse 1 BOM")
    lager_2_bedarfslager: str = Field(..., description="Warehouse 2 demand")
    lager_3_referenzen: str = Field(..., description="Warehouse 3 references")
    status: StatusEnum = Field(default=StatusEnum.OFFEN, description="Status")
    position: int = Field(..., description="Position number")
    bearbeitungsart: str = Field(default="", description="Processing type")
    vorgang_id: int = Field(..., description="Process ID")
    anzahl_aktion: int = Field(default=0, ge=0, description="Action count")
    kommisionierer: Optional[str] = Field(None, description="Picker")
    materialwagen: Optional[str] = Field(None, description="Material cart")
    anzahl_auf_wagen: Optional[int] = Field(None, ge=0, description="Quantity on cart")
    anzahl_fehlt: Optional[int] = Field(None, ge=0, description="Missing quantity")
    anzahl_beschaedigt: Optional[int] = Field(
        None, ge=0, description="Damaged quantity"
    )

    @validator("gewicht")
    def validate_weight(cls, v):
        """Validate weight is positive."""
        if v < 0:
            raise ValueError("Weight must be positive")
        return v

    @property
    def total_weight(self) -> float:
        """Calculate total weight for this line."""
        return self.gewicht * self.menge

    @property
    def available_quantity(self) -> int:
        """Calculate available quantity."""
        missing = self.anzahl_fehlt or 0
        damaged = self.anzahl_beschaedigt or 0
        return max(0, self.bestand - missing - damaged)

    @property
    def is_available(self) -> bool:
        """Check if article is available for picking."""
        return self.available_quantity >= self.menge


class ArticleCreate(BaseModel):
    """Model for creating a new article."""

    projekt_nr: str = Field(..., description="Project number")
    artikel: str = Field(..., description="Article number")
    artikel_bezeichnung: str = Field(..., description="Article description")
    menge: int = Field(..., ge=0, description="Quantity")
    einheit: str = Field(..., description="Unit")
    gewicht: float = Field(..., ge=0, description="Weight")
    lagerplatz: str = Field(..., description="Storage location")
    bestand: int = Field(..., ge=0, description="Current stock")
    wohin: str = Field(..., description="Destination")


class ArticleUpdate(BaseModel):
    """Model for updating an article."""

    status: Optional[StatusEnum] = Field(None, description="Status")
    anzahl_auf_wagen: Optional[int] = Field(None, ge=0, description="Quantity on cart")
    anzahl_fehlt: Optional[int] = Field(None, ge=0, description="Missing quantity")
    anzahl_beschaedigt: Optional[int] = Field(
        None, ge=0, description="Damaged quantity"
    )
    kommisionierer: Optional[str] = Field(None, description="Picker")
    materialwagen: Optional[str] = Field(None, description="Material cart")


class ArticleResponse(BaseModel):
    """Article response model."""

    artikel: str = Field(..., description="Article number")
    artikel_bezeichnung: str = Field(..., description="Article description")
    menge: int = Field(..., description="Required quantity")
    einheit: str = Field(..., description="Unit")
    gewicht: float = Field(..., description="Weight")
    lagerplatz: str = Field(..., description="Storage location")
    bestand: int = Field(..., description="Current stock")
    status: StatusEnum = Field(..., description="Status")
    total_weight: float = Field(..., description="Total weight")
    available_quantity: int = Field(..., description="Available quantity")
    is_available: bool = Field(..., description="Availability status")
    anzahl_auf_wagen: Optional[int] = Field(None, description="Quantity on cart")
    anzahl_fehlt: Optional[int] = Field(None, description="Missing quantity")
    anzahl_beschaedigt: Optional[int] = Field(None, description="Damaged quantity")


# EOF
