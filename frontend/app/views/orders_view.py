# File: frontend/app/views/orders_view.py
# Path: frontend/app/views/orders_view.py

"""
Orders management view.
"""

import logging
from nicegui import ui
from ..components.order_components import create_order_filter_component

logger = logging.getLogger(__name__)


def create_orders_view():
    """Create orders management view."""
    logger.info("Initialisiere Orders View")

    column = ui.column().classes("full-width q-pa-md")
    with column:
        ui.label("📋 Orders Management").classes("text-h4 q-mb-lg")

        # Filters
        create_order_filter_component()

        # Orders Table
        with ui.card().classes("full-width"):
            ui.label("No orders available").classes("text-grey-500")

    return column


# EOF
