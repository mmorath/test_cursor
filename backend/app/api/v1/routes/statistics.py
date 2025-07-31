# File: backend/app/api/v1/routes/statistics.py
# Path: backend/app/api/v1/routes/statistics.py

"""
Statistics API routes for the logistics management system.
"""

import logging
from fastapi import APIRouter, HTTPException, status, Request

from app.models import BaseResponse
from app.services.logistics_service import LogisticsService

router = APIRouter()
logger = logging.getLogger(__name__)


def get_logistics_service() -> LogisticsService:
    """Get logistics service instance."""
    return LogisticsService()


@router.get("/overview", response_model=BaseResponse)
async def get_system_overview(request: Request):
    """Get system overview statistics."""
    logger.info("📥 API v1 - GET /statistics/overview")

    try:
        service = get_logistics_service()
        overview = service.get_system_overview()

        return BaseResponse(
            status="success",
            message="System overview retrieved successfully",
            data=overview
        )

    except Exception as e:
        logger.error("❌ Error getting system overview: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


# EOF