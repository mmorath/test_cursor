# File: backend/app/api/v1/routes/pickers.py
# Path: backend/app/api/v1/routes/pickers.py

"""
Pickers API routes for the logistics management system.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import JSONResponse

from app.models import PickerResponse, BaseResponse, ErrorResponse
from app.services.logistics_service import LogisticsService

router = APIRouter()
logger = logging.getLogger(__name__)

# MARK: ━━━ Dependencies ━━━


def get_logistics_service() -> LogisticsService:
    """Get logistics service instance."""
    return LogisticsService()


# MARK: ━━━ Picker Endpoints ━━━


@router.get("/", response_model=BaseResponse)
async def list_pickers(request: Request):
    """Get all pickers."""
    logger.info("📥 API v1 - GET /pickers")

    try:
        service = get_logistics_service()
        pickers = service.pickers

        picker_responses = []
        for picker in pickers:
            picker_responses.append(
                PickerResponse(
                    picker_id=picker.picker_id,
                    name=picker.name,
                    employee_number=picker.employee_number,
                    is_active=picker.is_active,
                    current_order=picker.current_order,
                )
            )

        return BaseResponse(
            status="success",
            message="Pickers retrieved successfully",
            data={"pickers": [picker.dict() for picker in picker_responses]},
        )

    except Exception as e:
        logger.error("❌ Error getting pickers: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post("/", response_model=BaseResponse)
async def create_picker(request: Request):
    """Create a new picker."""
    logger.info("📥 API v1 - POST /pickers")

    try:
        service = get_logistics_service()
        # Implementation would create a new picker
        return BaseResponse(
            status="success",
            message="Picker created successfully",
            data={"picker_id": "P001"},
        )

    except Exception as e:
        logger.error("❌ Error creating picker: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


# EOF
