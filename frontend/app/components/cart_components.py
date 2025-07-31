# File: frontend/app/components/cart_components.py
# Path: frontend/app/components/cart_components.py

"""
Cart-related UI components.
"""

import logging
from nicegui import ui

logger = logging.getLogger(__name__)


def create_cart_form_component(on_submit=None):
    """Create cart form component."""
    logger.info("Initialisiere Cart Form Component")

    with ui.card().classes("full-width"):
        ui.label("🛒 Add New Cart").classes("text-h6 q-mb-md")

        capacity = ui.number(
            "Capacity (kg)",
            min=0,
            value=100,
            validation={"Capacity must be positive": lambda value: value > 0},
        ).classes("full-width q-mb-md")

        with ui.row():
            ui.button("Cancel", on_click=lambda: ui.close_dialog()).classes(
                "bg-grey-500 q-mr-sm"
            )
            ui.button(
                "Add", on_click=lambda: handle_cart_submit(capacity.value, on_submit)
            ).classes("bg-green-500")


def handle_cart_submit(capacity: float, on_submit):
    """Handle cart form submission."""
    logger.info(f"Submitting cart with capacity: {capacity}")

    if capacity <= 0:
        ui.notify("Capacity must be positive", type="error")
        return

    if on_submit:
        on_submit(capacity)

    ui.close_dialog()
    ui.notify("✅ Cart added successfully", type="positive")


# EOF
