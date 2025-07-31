# File: frontend/main.py
# Path: frontend/main.py

"""
Main entry point for the frontend application.
Only initialization, no business logic.
"""

import logging
from nicegui import ui

from app.logger import initialize_logging, get_logger
from app.routes import setup_routes
from config import settings

# MARK: ━━━ Logging Setup ━━━

initialize_logging()
logger = get_logger(__name__)

# MARK: ━━━ Application Initialization ━━━

def initialize_application():
    """Initialize the frontend application."""
    logger.info("🚀 Starting Logistics Management System Frontend")
    logger.info(f"📡 Frontend will be available at http://{settings.host}:{settings.port}")

    # Setup routes
    setup_routes()

    logger.info("✅ Frontend initialized successfully")


# MARK: ━━━ Main Application ━━━

if __name__ in {"__main__", "__mp_main__"}:
    initialize_application()

    ui.run(
        title=settings.app_name,
        port=settings.port,
        host=settings.host,
        reload=settings.debug,
        show=True
    )

# EOF