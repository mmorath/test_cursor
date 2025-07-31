# File: frontend/app/views/pickers_view.py
# Path: frontend/app/views/pickers_view.py

"""
Pickers management view.
"""

import logging
from nicegui import ui

logger = logging.getLogger(__name__)


def create_pickers_view():
    """Create pickers management view."""
    logger.info("Initialisiere Pickers View")

    with ui.column().classes("full-width q-pa-md"):
        ui.label("👥 Pickers Management").classes("text-h4 q-mb-lg")

        with ui.row().classes("full-width q-mb-md"):
            ui.button("➕ Add Picker", on_click=add_picker).classes("bg-green-600")

        # Pickers Grid
        with ui.row().classes("full-width q-gutter-md"):
            ui.label("No pickers available").classes("text-grey-500")


def add_picker():
    """Add new picker dialog."""
    logger.info("Opening add picker dialog")
    ui.notify("➕ Add picker feature coming soon", type="info")


# EOF