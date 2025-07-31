# File: frontend/app/routes/routes.py
# Path: frontend/app/routes/routes.py

"""
Page routing configuration for the frontend application.
"""

import logging
from nicegui import ui
from ..views import (
    create_dashboard_view,
    create_orders_view,
    create_pickers_view,
    create_carts_view,
)

logger = logging.getLogger(__name__)


def setup_routes():
    """Setup all application routes."""
    logger.info("Setting up application routes")

    @ui.page("/")
    def dashboard_page():
        """Dashboard page."""
        logger.info("📥 Route: Dashboard page")
        create_header()
        create_sidebar()
        create_dashboard_view()

    @ui.page("/orders")
    def orders_page():
        """Orders management page."""
        logger.info("📥 Route: Orders page")
        create_header()
        create_sidebar()
        create_orders_view()

    @ui.page("/pickers")
    def pickers_page():
        """Pickers management page."""
        logger.info("📥 Route: Pickers page")
        create_header()
        create_sidebar()
        create_pickers_view()

    @ui.page("/carts")
    def carts_page():
        """Carts management page."""
        logger.info("📥 Route: Carts page")
        create_header()
        create_sidebar()
        create_carts_view()


def create_header():
    """Create application header."""
    with ui.header().classes("bg-blue-500 text-white"):
        ui.label("🏭 Logistics Management System").classes("text-h6")
        ui.space()
        with ui.row().classes("items-center"):
            ui.button("🔄 Refresh", on_click=refresh_data).classes(
                "bg-blue-600"
            )
            ui.button("📊 Statistics", on_click=show_statistics).classes(
                "bg-green-600"
            )


def create_sidebar():
    """Create navigation sidebar."""
    with ui.left_drawer().classes("bg-grey-100"):
        ui.label("Navigation").classes("text-h6 q-mb-md")

        ui.button("📋 Orders", on_click=lambda: ui.open("/orders")).classes(
            "full-width q-mb-sm"
        )
        ui.button("👥 Pickers", on_click=lambda: ui.open("/pickers")).classes(
            "full-width q-mb-sm"
        )
        ui.button("🛒 Carts", on_click=lambda: ui.open("/carts")).classes(
            "full-width q-mb-sm"
        )
        ui.button("📈 Dashboard", on_click=lambda: ui.open("/")).classes(
            "full-width q-mb-sm"
        )


def refresh_data():
    """Refresh application data."""
    logger.info("Refreshing application data")
    ui.notify("🔄 Refreshing data...", type="info")


def show_statistics():
    """Show detailed statistics."""
    logger.info("Showing detailed statistics")
    ui.notify("📊 Statistics feature coming soon", type="info")


# EOF
