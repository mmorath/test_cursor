# File: frontend/tests/conftest.py
# Path: frontend/tests/conftest.py

"""
Pytest configuration and shared fixtures for frontend tests.
"""

import pytest
import asyncio
from nicegui import ui
from httpx import AsyncClient

# MARK: ━━━ Pytest Configuration ━━━

pytest_plugins = ["pytest_asyncio"]


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# MARK: ━━━ NiceGUI Test Setup ━━━

@pytest.fixture
def nicegui_app():
    """Create a NiceGUI app instance for testing."""
    # Initialize NiceGUI app
    ui.run = lambda **kwargs: None  # Mock ui.run for testing
    return ui


# MARK: ━━━ HTTP Client Fixtures ━━━

@pytest.fixture
async def api_client():
    """Create an async HTTP client for API testing."""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        yield client


# MARK: ━━━ Test Data Fixtures ━━━

@pytest.fixture
def sample_order_data():
    """Sample order data for frontend testing."""
    return {
        "order_id": "ORDER-054536-001",
        "project_number": "054536",
        "priority": 5,
        "status": "Offen",
        "assigned_picker": None,
        "completion_percentage": 0.0
    }


@pytest.fixture
def sample_picker_data():
    """Sample picker data for frontend testing."""
    return {
        "picker_id": "P001",
        "name": "John Doe",
        "employee_number": "EMP001",
        "is_active": True,
        "current_order": None
    }


@pytest.fixture
def sample_cart_data():
    """Sample cart data for frontend testing."""
    return {
        "cart_id": "C001",
        "capacity": 100.0,
        "current_weight": 0.0,
        "is_available": True,
        "assigned_picker": None
    }


@pytest.fixture
def sample_statistics_data():
    """Sample statistics data for frontend testing."""
    return {
        "total_orders": 10,
        "open_orders": 5,
        "completed_orders": 5,
        "total_articles": 50,
        "picked_articles": 25,
        "completion_rate": 50.0,
        "efficiency_score": 75.0
    }


# EOF