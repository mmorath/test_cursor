# File: frontend/tests/test_validators.py
# Path: frontend/tests/test_validators.py

"""
Test: Frontend Validator Tests
Description:
    Tests the input validation functions.
    Verifies validation logic and error handling.

Author: Matthias Morath
Created: 2025-01-28
"""

# MARK: ━━━ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import logging

from app.validators.order_validators import validate_project_number, validate_priority
from app.validators.picker_validators import validate_picker_name, validate_employee_number

# MARK: ━━━ Logger ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logger = logging.getLogger(__name__)


# MARK: ━━━ Test Cases ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_validate_project_number():
    """Test project number validation."""
    logger.info("Testing project number validation")

    # Valid project numbers
    assert validate_project_number("054536") is None
    assert validate_project_number("123456") is None

    # Invalid project numbers
    assert validate_project_number("") == "Project number is required"
    assert validate_project_number("12345") == "Project number must be 6 digits"
    assert validate_project_number("1234567") == "Project number must be 6 digits"
    assert validate_project_number("abc123") == "Project number must be 6 digits"

    logger.info("Project number validation test passed")


def test_validate_priority():
    """Test priority validation."""
    logger.info("Testing priority validation")

    # Valid priorities
    assert validate_priority(1) is None
    assert validate_priority(5) is None
    assert validate_priority(10) is None

    # Invalid priorities
    assert validate_priority(0) == "Priority must be between 1 and 10"
    assert validate_priority(11) == "Priority must be between 1 and 10"
    assert validate_priority(-1) == "Priority must be between 1 and 10"

    logger.info("Priority validation test passed")


def test_validate_picker_name():
    """Test picker name validation."""
    logger.info("Testing picker name validation")

    # Valid names
    assert validate_picker_name("John Doe") is None
    assert validate_picker_name("A") is None  # 2 chars minimum
    assert validate_picker_name("A" * 50) is None  # 50 chars maximum

    # Invalid names
    assert validate_picker_name("") == "Picker name is required"
    assert validate_picker_name("A") == "Picker name must be at least 2 characters"
    assert validate_picker_name("A" * 51) == "Picker name must be less than 50 characters"

    logger.info("Picker name validation test passed")


def test_validate_employee_number():
    """Test employee number validation."""
    logger.info("Testing employee number validation")

    # Valid employee numbers
    assert validate_employee_number("EMP001") is None
    assert validate_employee_number("EMP999") is None

    # Invalid employee numbers
    assert validate_employee_number("") == "Employee number is required"
    assert validate_employee_number("EMP01") == "Employee number must be in format EMP001"
    assert validate_employee_number("EMP0001") == "Employee number must be in format EMP001"
    assert validate_employee_number("emp001") == "Employee number must be in format EMP001"
    assert validate_employee_number("ABC001") == "Employee number must be in format EMP001"

    logger.info("Employee number validation test passed")


# EOF