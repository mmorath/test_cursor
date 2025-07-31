# File: frontend/app/views/dashboard_view.py
# Path: frontend/app/views/dashboard_view.py

"""
Dashboard view for the logistics management system.
"""

import logging
from nicegui import ui
from ..components.statistics_components import create_statistics_card_component

logger = logging.getLogger(__name__)


def create_dashboard_view():
    """Create main dashboard view."""
    logger.info("Initialisiere Dashboard View")

    with ui.column().classes("full-width q-pa-md"):
        ui.label("📊 System Dashboard").classes("text-h4 q-mb-lg")

        # Statistics Cards
        with ui.row().classes("full-width q-gutter-md"):
            create_statistics_card_component("📦 Total Orders", "0", "bg-blue-100")
            create_statistics_card_component("✅ Completed Orders", "0", "bg-green-100")
            create_statistics_card_component("⏳ Open Orders", "0", "bg-orange-100")
            create_statistics_card_component("📈 Completion Rate", "0%", "bg-purple-100")

        # Recent Orders
        with ui.card().classes("full-width q-mt-lg"):
            ui.label("📋 Recent Orders").classes("text-h6 q-mb-md")
            ui.label("No orders available").classes("text-grey-500")


# EOF