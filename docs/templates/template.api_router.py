# File: app/api/v1/routes/route_{{ resource }}.py
# -*- coding:utf-8 -*-
"""
Router: {{ resource | capitalize }} API
Description:
    API-Endpunkte zur Verwaltung von {{ resource }}.
    Versioniert unter /api/v1/{{ resource }}

Author: Matthias Morath
Created: {{ created }}
"""

# MARK: ━━━ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import logging
from fastapi import APIRouter, HTTPException, status
from typing import Union
from ..models.{{ resource }}_models import {{ resource | capitalize }}Input, {{ resource | capitalize }}Output
from ..models.model_response import ResponseModel, ErrorResponse

# MARK: ━━━ Logger ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logger = logging.getLogger(__name__)

# MARK: ━━━ Router Definition ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
router = APIRouter(
    prefix="/api/v1/{{ resource }}",
    tags=["{{ resource | capitalize }}"]
)

# MARK: ━━━ Routes ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@router.post(
    "/validate",
    response_model=Union[ResponseModel[{{ resource | capitalize }}Output], ErrorResponse],
    status_code=200,
    summary="Validiere Eingabedaten",
    description="Validiert die übermittelten {{ resource }}-Daten und gibt das Ergebnis zurück."
)
def validate_{{ resource }}(payload: {{ resource | capitalize }}Input) -> Union[ResponseModel[{{ resource | capitalize }}Output], ErrorResponse]:
    """
    Validiert übergebene Eingabedaten.

    Args:
        payload ({{ resource | capitalize }}Input): Eingabedaten zur Validierung.

    Returns:
        Union[ResponseModel[{{ resource | capitalize }}Output], ErrorResponse]: Ergebnis.
    """
    try:
        logger.debug("🔍 Eingabe empfangen: %s", payload.model_dump())
        result = {"valid": True, "input": payload.model_dump()}
        logger.info("✅ Validierung erfolgreich")
        return ResponseModel(success=True, data=result, error=None)
    except Exception as e:
        logger.error("❌ Validierung fehlgeschlagen: %s", str(e))
        return ErrorResponse(
            success=False,
            message="Fehler bei Validierung",
            details=str(e),
            code=500
        )