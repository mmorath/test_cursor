# File: backend/tests/conftest.py
# Path: backend/tests/conftest.py

"""
Pytest configuration and shared fixtures for backend tests.
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient

from main import app
from app.services.logistics_service import LogisticsService
from app.services.data_service import DataService

# MARK: ━━━ Pytest Configuration ━━━

pytest_plugins = ["pytest_asyncio"]


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# MARK: ━━━ Test Clients ━━━

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
async def async_client():
    """Create an async test client for the FastAPI application."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# MARK: ━━━ Service Fixtures ━━━

@pytest.fixture
def logistics_service():
    """Create a logistics service instance for testing."""
    return LogisticsService()


@pytest.fixture
def data_service():
    """Create a data service instance for testing."""
    return DataService()


# MARK: ━━━ Test Data Fixtures ━━━

@pytest.fixture
def sample_article_data():
    """Sample article data for testing."""
    return {
        "projekt_nr": "054536",
        "abteilungsgruppe": "LOGISTIK ALLES",
        "kostenstelle": "2KF",
        "baugruppe": "919713008",
        "artikel": "388303408",
        "artikel_bezeichnung": "SPANNPRATZE GS18NIMOCR36 FLZN",
        "menge": 3,
        "einheit": "stk",
        "gewicht": 0.771,
        "lagerplatz": "23IZ022A",
        "filter": "23I",
        "bestand": 596,
        "wohin": "SHL-SHV--V01",
        "lz": "",
        "lager_1_stueckliste": "MZS",
        "lager_2_bedarfslager": "MZS",
        "lager_3_referenzen": "SHL",
        "status": "Offen",
        "position": 578954208,
        "bearbeitungsart": "",
        "vorgang_id": 127099,
        "anzahl_aktion": 0
    }


@pytest.fixture
def sample_project_data():
    """Sample project data for testing."""
    return {
        "projekt_nr": "054536",
        "articles": [
            {
                "projekt_nr": "054536",
                "abteilungsgruppe": "LOGISTIK ALLES",
                "kostenstelle": "2KF",
                "baugruppe": "919713008",
                "artikel": "388303408",
                "artikel_bezeichnung": "SPANNPRATZE GS18NIMOCR36 FLZN",
                "menge": 3,
                "einheit": "stk",
                "gewicht": 0.771,
                "lagerplatz": "23IZ022A",
                "filter": "23I",
                "bestand": 596,
                "wohin": "SHL-SHV--V01",
                "lz": "",
                "lager_1_stueckliste": "MZS",
                "lager_2_bedarfslager": "MZS",
                "lager_3_referenzen": "SHL",
                "status": "Offen",
                "position": 578954208,
                "bearbeitungsart": "",
                "vorgang_id": 127099,
                "anzahl_aktion": 0
            }
        ]
    }


@pytest.fixture
def sample_order_data():
    """Sample order data for testing."""
    return {
        "order_id": "ORDER-054536-001",
        "project_number": "054536",
        "priority": 5,
        "status": "Offen"
    }


@pytest.fixture
def sample_picker_data():
    """Sample picker data for testing."""
    return {
        "picker_id": "P001",
        "name": "John Doe",
        "employee_number": "EMP001",
        "is_active": True
    }


@pytest.fixture
def sample_cart_data():
    """Sample cart data for testing."""
    return {
        "cart_id": "C001",
        "capacity": 100.0,
        "current_weight": 0.0,
        "is_available": True
    }


# EOF