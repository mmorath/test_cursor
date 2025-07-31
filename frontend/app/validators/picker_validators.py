# File: frontend/app/validators/picker_validators.py
# Path: frontend/app/validators/picker_validators.py

"""
Picker validation functions.
"""

import re
from typing import Optional


def validate_picker_name(name: str) -> Optional[str]:
    """Validate picker name."""
    if not name:
        return "Picker name is required"

    if len(name) < 2:
        return "Picker name must be at least 2 characters"

    if len(name) > 50:
        return "Picker name must be less than 50 characters"

    return None


def validate_employee_number(employee_number: str) -> Optional[str]:
    """Validate employee number format."""
    if not employee_number:
        return "Employee number is required"

    if not re.match(r"^EMP\d{3}$", employee_number):
        return "Employee number must be in format EMP001"

    return None


# EOF
