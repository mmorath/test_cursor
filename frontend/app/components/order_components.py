# File: frontend/app/components/order_components.py
# Path: frontend/app/components/order_components.py

"""
Order-related UI components.
"""

import logging
from nicegui import ui
from ..validators.order_validators import validate_project_number, validate_priority

logger = logging.getLogger(__name__)


def create_order_form_component(on_submit=None):
    """Create order form component."""
    logger.info("Initialisiere Order Form Component")

    with ui.card().classes("full-width"):
        ui.label("➕ Create New Order").classes("text-h6 q-mb-md")

        project_number = ui.input(
            "Project Number",
            validation={
                "Project number is required": lambda value: bool(value),
                "Must be 6 digits": lambda value: validate_project_number(value)
                is None,
            },
        ).classes("full-width q-mb-md")

        priority = ui.select("Priority", options=[1, 2, 3, 4, 5], value=1).classes(
            "full-width q-mb-md"
        )

        with ui.row():
            ui.button("Cancel", on_click=lambda: ui.close_dialog()).classes(
                "bg-grey-500 q-mr-sm"
            )
            ui.button(
                "Create",
                on_click=lambda: handle_order_submit(
                    project_number.value, priority.value, on_submit
                ),
            ).classes("bg-green-500")


def create_order_filter_component(on_filter=None):
    """Create order filter component."""
    logger.info("Initialisiere Order Filter Component")

    with ui.card().classes("full-width"):
        ui.label("🔍 Filter Orders").classes("text-h6 q-mb-md")

        status_filter = ui.select(
            "Status",
            options=["All", "Offen", "In Bearbeitung", "Abgeschlossen"],
            value="All",
        ).classes("q-mr-md")

        priority_filter = ui.select(
            "Priority", options=["All", 1, 2, 3, 4, 5], value="All"
        ).classes("q-mr-md")

        ui.button(
            "Apply Filter",
            on_click=lambda: handle_filter_apply(
                status_filter.value, priority_filter.value, on_filter
            ),
        ).classes("bg-blue-500")


def handle_order_submit(project_number: str, priority: int, on_submit):
    """Handle order form submission."""
    logger.info(f"Submitting order: {project_number}, priority: {priority}")

    # Validate inputs
    project_error = validate_project_number(project_number)
    priority_error = validate_priority(priority)

    if project_error:
        ui.notify(project_error, type="error")
        return

    if priority_error:
        ui.notify(priority_error, type="error")
        return

    if on_submit:
        on_submit(project_number, priority)

    ui.close_dialog()
    ui.notify("✅ Order created successfully", type="positive")


def handle_filter_apply(status: str, priority: int, on_filter):
    """Handle filter application."""
    logger.info(f"Applying filter: status={status}, priority={priority}")

    if on_filter:
        on_filter(status, priority)

    ui.notify("🔍 Filter applied", type="info")


# EOF
