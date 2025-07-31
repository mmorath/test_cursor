# File: frontend/app/components/statistics_components.py
# Path: frontend/app/components/statistics_components.py

"""
Statistics-related UI components.
"""

import logging
from nicegui import ui

logger = logging.getLogger(__name__)


def create_statistics_card_component(title: str, value: str, bg_class: str):
    """Create statistics card component."""
    logger.debug(f"Creating statistics card: {title}")

    with ui.card().classes(bg_class):
        ui.label(title).classes("text-h6")
        ui.label(value).classes("text-h4")


# EOF