# File: frontend/tests/test_views.py
# Path: frontend/tests/test_views.py

"""
Test: Frontend View Tests
Description:
    Tests the NiceGUI views and their functionality.
    Verifies view creation and basic UI structure.

Author: Matthias Morath
Created: 2025-01-28
"""

# MARK: ━━━ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import logging

from app.views.dashboard_view import create_dashboard_view
from app.views.orders_view import create_orders_view
from app.views.pickers_view import create_pickers_view
from app.views.carts_view import create_carts_view

# MARK: ━━━ Logger ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logger = logging.getLogger(__name__)


# MARK: ━━━ Test Cases ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def test_dashboard_view_creation():
    """Test that dashboard view can be created."""
    logger.info("Testing dashboard view creation")

    # Create dashboard view
    view = create_dashboard_view()

    # View should be created without errors
    assert view is not None
    logger.info("Dashboard view creation test passed")


def test_orders_view_creation():
    """Test that orders view can be created."""
    logger.info("Testing orders view creation")

    # Create orders view
    view = create_orders_view()

    # View should be created without errors
    assert view is not None
    logger.info("Orders view creation test passed")


def test_pickers_view_creation():
    """Test that pickers view can be created."""
    logger.info("Testing pickers view creation")

    # Create pickers view
    view = create_pickers_view()

    # View should be created without errors
    assert view is not None
    logger.info("Pickers view creation test passed")


def test_carts_view_creation():
    """Test that carts view can be created."""
    logger.info("Testing carts view creation")

    # Create carts view
    view = create_carts_view()

    # View should be created without errors
    assert view is not None
    logger.info("Carts view creation test passed")


# EOF
