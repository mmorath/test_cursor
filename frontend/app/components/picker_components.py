# File: frontend/app/components/picker_components.py
# Path: frontend/app/components/picker_components.py

"""
Picker-related UI components.
"""

import logging
from nicegui import ui
from ..validators.picker_validators import (
    validate_picker_name,
    validate_employee_number,
)

logger = logging.getLogger(__name__)


def create_picker_form_component(on_submit=None):
    """Create picker form component."""
    logger.info("Initialisiere Picker Form Component")

    with ui.card().classes("full-width"):
        ui.label("👤 Add New Picker").classes("text-h6 q-mb-md")

        name = ui.input(
            "Name",
            validation={
                "Name is required": lambda value: bool(value),
                "Must be 2-50 characters": lambda value: validate_picker_name(value)
                is None,
            },
        ).classes("full-width q-mb-md")

        employee_number = ui.input(
            "Employee Number",
            validation={
                "Employee number is required": lambda value: bool(value),
                "Must be in format EMP001": lambda value: validate_employee_number(
                    value
                )
                is None,
            },
        ).classes("full-width q-mb-md")

        with ui.row():
            ui.button("Cancel", on_click=lambda: ui.close_dialog()).classes(
                "bg-grey-500 q-mr-sm"
            )
            ui.button(
                "Add",
                on_click=lambda: handle_picker_submit(
                    name.value, employee_number.value, on_submit
                ),
            ).classes("bg-green-500")


def handle_picker_submit(name: str, employee_number: str, on_submit):
    """Handle picker form submission."""
    logger.info(f"Submitting picker: {name}, employee: {employee_number}")

    # Validate inputs
    name_error = validate_picker_name(name)
    employee_error = validate_employee_number(employee_number)

    if name_error:
        ui.notify(name_error, type="error")
        return

    if employee_error:
        ui.notify(employee_error, type="error")
        return

    if on_submit:
        on_submit(name, employee_number)

    ui.close_dialog()
    ui.notify("✅ Picker added successfully", type="positive")


# EOF
