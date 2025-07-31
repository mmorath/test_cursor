# File: backend/app/api/v1/routes/orders.py
# Path: backend/app/api/v1/routes/orders.py

"""
Route: /api/v1/orders

Description:
    API endpoints for managing picking orders.

Version: v1
Author: Matthias Morath
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Request, Query
from fastapi.responses import JSONResponse

from app.models import (
    OrderResponse,
    OrderList,
    BaseResponse,
    ErrorResponse,
    PaginationParams,
)
from app.services.logistics_service import LogisticsService

router = APIRouter()
logger = logging.getLogger(__name__)

# MARK: ━━━ Dependencies ━━━


def get_logistics_service() -> LogisticsService:
    """Get logistics service instance."""
    # In a real app, this would come from dependency injection
    return LogisticsService()


# MARK: ━━━ Order Endpoints ━━━


@router.get("/", response_model=BaseResponse)
async def list_orders(
    request: Request,
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
):
    """Get all orders with optional filtering and pagination."""
    logger.info("📥 API v1 - GET /orders")

    try:
        service = get_logistics_service()

        # Filter orders by status if specified
        if status_filter:
            orders = [
                order
                for order in service.orders
                if order.status.value == status_filter
            ]
        else:
            orders = service.orders

        # Pagination
        total = len(orders)
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        paginated_orders = orders[start_idx:end_idx]

        # Convert to response models
        order_responses = []
        for order in paginated_orders:
            order_responses.append(
                OrderResponse(
                    order_id=order.order_id,
                    project_number=order.project.projekt_nr,
                    status=order.status,
                    priority=order.priority,
                    assigned_picker=order.assigned_picker,
                    created_at=order.created_at,
                    completion_percentage=order.completion_percentage,
                    total_articles=len(order.project.articles),
                    completed_articles=len(order.project.completed_articles),
                    total_weight=order.project.total_weight,
                    is_complete=order.is_complete,
                )
            )

        return BaseResponse(
            status="success",
            message="Orders retrieved successfully",
            data={
                "orders": [order.dict() for order in order_responses],
                "pagination": {
                    "page": page,
                    "size": size,
                    "total": total,
                    "pages": (total + size - 1) // size,
                },
            },
        )

    except Exception as e:
        logger.error("❌ Error getting orders: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.get("/{order_id}", response_model=BaseResponse)
async def get_order(order_id: str, request: Request):
    """Get specific order by ID."""
    logger.info("📥 API v1 - GET /orders/%s", order_id)

    try:
        service = get_logistics_service()
        order = service.get_order_by_id(order_id)

        if not order:
            return JSONResponse(
                status_code=404,
                content=ErrorResponse(
                    status="error",
                    message="Order not found",
                    details=f"No order found with id {order_id}",
                    code=404,
                ).dict(),
            )

        order_response = OrderResponse(
            order_id=order.order_id,
            project_number=order.project.projekt_nr,
            status=order.status,
            priority=order.priority,
            assigned_picker=order.assigned_picker,
            created_at=order.created_at,
            completion_percentage=order.completion_percentage,
            total_articles=len(order.project.articles),
            completed_articles=len(order.project.completed_articles),
            total_weight=order.project.total_weight,
            is_complete=order.is_complete,
        )

        return BaseResponse(
            status="success",
            message="Order retrieved successfully",
            data=order_response.dict(),
        )

    except Exception as e:
        logger.error("❌ Error getting order %s: %s", order_id, str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post("/{order_id}/assign", response_model=BaseResponse)
async def assign_order(order_id: str, picker_id: str, request: Request):
    """Assign an order to a picker."""
    logger.info("📥 API v1 - POST /orders/%s/assign", order_id)

    try:
        service = get_logistics_service()
        success = service.assign_order_to_picker(order_id, picker_id)

        if not success:
            return JSONResponse(
                status_code=400,
                content=ErrorResponse(
                    status="error",
                    message="Failed to assign order",
                    details="Order or picker not found, or assignment not possible",
                    code=400,
                ).dict(),
            )

        return BaseResponse(
            status="success",
            message=f"Order {order_id} assigned to picker {picker_id}",
            data={"order_id": order_id, "picker_id": picker_id},
        )

    except Exception as e:
        logger.error("❌ Error assigning order %s: %s", order_id, str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post("/{order_id}/pick", response_model=BaseResponse)
async def pick_article(
    order_id: str,
    article_id: str,
    quantity: int,
    picker_id: str,
    request: Request,
):
    """Record picking of an article."""
    logger.info("📥 API v1 - POST /orders/%s/pick", order_id)

    try:
        service = get_logistics_service()
        success = service.pick_article(
            order_id, article_id, quantity, picker_id
        )

        if not success:
            return JSONResponse(
                status_code=400,
                content=ErrorResponse(
                    status="error",
                    message="Failed to pick article",
                    details="Article not found or picking not possible",
                    code=400,
                ).dict(),
            )

        return BaseResponse(
            status="success",
            message=f"Picked {quantity} of article {article_id}",
            data={
                "order_id": order_id,
                "article_id": article_id,
                "quantity": quantity,
                "picker_id": picker_id,
            },
        )

    except Exception as e:
        logger.error("❌ Error picking article %s: %s", article_id, str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post("/{order_id}/complete", response_model=BaseResponse)
async def complete_order(order_id: str, request: Request):
    """Mark an order as completed."""
    logger.info("📥 API v1 - POST /orders/%s/complete", order_id)

    try:
        service = get_logistics_service()
        success = service.complete_order(order_id)

        if not success:
            return JSONResponse(
                status_code=400,
                content=ErrorResponse(
                    status="error",
                    message="Failed to complete order",
                    details="Order not found or not ready for completion",
                    code=400,
                ).dict(),
            )

        return BaseResponse(
            status="success",
            message=f"Order {order_id} completed",
            data={"order_id": order_id},
        )

    except Exception as e:
        logger.error("❌ Error completing order %s: %s", order_id, str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


# EOF
