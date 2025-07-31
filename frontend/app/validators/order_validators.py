# File: frontend/app/validators/order_validators.py
# Path: frontend/app/validators/order_validators.py

"""
Order validation functions.
"""

import re
from typing import Optional


def validate_project_number(project_number: str) -> Optional[str]:
    """Validate project number format."""
    if not project_number:
        return "Project number is required"

    if not re.match(r'^\d{6}$', project_number):
        return "Project number must be 6 digits"

    return None


def validate_priority(priority: int) -> Optional[str]:
    """Validate priority value."""
    if not isinstance(priority, int):
        return "Priority must be a number"

    if priority < 1 or priority > 10:
        return "Priority must be between 1 and 10"

    return None


# EOF