# File: frontend/tests/test_components.py
# Path: frontend/tests/test_components.py

"""
Test: Frontend Component Tests
Description:
    Tests the NiceGUI components and their functionality.
    Verifies component creation, validation, and user interactions.

Author: Matthias Morath
Created: 2025-01-28
"""

# MARK: ━━━ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import logging
from nicegui import ui

from app.components.order_components import create_order_form_component
from app.components.picker_components import create_picker_form_component
from app.components.cart_components import create_cart_form_component
from app.components.statistics_components import create_statistics_card_component

# MARK: ━━━ Logger ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logger = logging.getLogger(__name__)


# MARK: ━━━ Test Cases ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_order_form_component_creation():
    """Test that order form component can be created."""
    logger.info("Testing order form component creation")

    # Mock callback function
    def mock_submit(project_number: str, priority: int):
        logger.info(f"Mock submit: {project_number}, {priority}")

    # Create component
    component = create_order_form_component(on_submit=mock_submit)

    # Component should be created without errors
    assert component is not None
    logger.info("Order form component creation test passed")


def test_picker_form_component_creation():
    """Test that picker form component can be created."""
    logger.info("Testing picker form component creation")

    # Mock callback function
    def mock_submit(name: str, employee_number: str):
        logger.info(f"Mock submit: {name}, {employee_number}")

    # Create component
    component = create_picker_form_component(on_submit=mock_submit)

    # Component should be created without errors
    assert component is not None
    logger.info("Picker form component creation test passed")


def test_cart_form_component_creation():
    """Test that cart form component can be created."""
    logger.info("Testing cart form component creation")

    # Mock callback function
    def mock_submit(capacity: float):
        logger.info(f"Mock submit: {capacity}")

    # Create component
    component = create_cart_form_component(on_submit=mock_submit)

    # Component should be created without errors
    assert component is not None
    logger.info("Cart form component creation test passed")


def test_statistics_card_component_creation():
    """Test that statistics card component can be created."""
    logger.info("Testing statistics card component creation")

    # Create component
    component = create_statistics_card_component(
        "Test Title",
        "Test Value",
        "bg-blue-100"
    )

    # Component should be created without errors
    assert component is not None
    logger.info("Statistics card component creation test passed")


def test_order_filter_component_creation():
    """Test that order filter component can be created."""
    logger.info("Testing order filter component creation")

    # Mock callback function
    def mock_filter(status: str, priority: int):
        logger.info(f"Mock filter: {status}, {priority}")

    # Import the function
    from app.components.order_components import create_order_filter_component

    # Create component
    component = create_order_filter_component(on_filter=mock_filter)

    # Component should be created without errors
    assert component is not None
    logger.info("Order filter component creation test passed")


# EOF