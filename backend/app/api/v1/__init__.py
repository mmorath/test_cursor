# File: backend/app/api/v1/__init__.py
# Path: backend/app/api/v1/__init__.py

"""
API v1 package for the logistics management system.
"""

from fastapi import APIRouter
from .routes import orders, pickers, carts, statistics

# MARK: ━━━ API v1 Router ━━━

api_router = APIRouter(prefix="/api/v1", tags=["v1"])

# Include all route modules
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(pickers.router, prefix="/pickers", tags=["pickers"])
api_router.include_router(carts.router, prefix="/carts", tags=["carts"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"])

# EOF