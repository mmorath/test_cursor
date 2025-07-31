# File: backend/app/api/v1/routes/carts.py
# Path: backend/app/api/v1/routes/carts.py

"""
Carts API routes for the logistics management system.
"""

import logging
from fastapi import APIRouter, HTTPException, status, Request

from app.models import (
    CartResponse, BaseResponse
)
from app.services.logistics_service import LogisticsService

router = APIRouter()
logger = logging.getLogger(__name__)


def get_logistics_service() -> LogisticsService:
    """Get logistics service instance."""
    return LogisticsService()


@router.get("/", response_model=BaseResponse)
async def list_carts(request: Request):
    """Get all carts."""
    logger.info("📥 API v1 - GET /carts")

    try:
        service = get_logistics_service()
        carts = service.carts

        cart_responses = []
        for cart in carts:
            cart_responses.append(CartResponse(
                cart_id=cart.cart_id,
                capacity=cart.capacity,
                current_weight=cart.current_weight,
                is_available=cart.is_available,
                assigned_picker=cart.assigned_picker
            ))

        return BaseResponse(
            status="success",
            message="Carts retrieved successfully",
            data={"carts": [cart.dict() for cart in cart_responses]}
        )

    except Exception as e:
        logger.error("❌ Error getting carts: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.post("/", response_model=BaseResponse)
async def create_cart(request: Request):
    """Create a new cart."""
    logger.info("📥 API v1 - POST /carts")

    try:
        # Implementation would create a new cart
        return BaseResponse(
            status="success",
            message="Cart created successfully",
            data={"cart_id": "C001"}
        )

    except Exception as e:
        logger.error("❌ Error creating cart: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


# EOF