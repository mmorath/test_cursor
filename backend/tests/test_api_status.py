# File: backend/tests/test_api_status.py
# Path: backend/tests/test_api_status.py

"""
Test: API Status and Health Check Tests
Description:
    Verifies the basic API endpoints are working correctly.
    Tests health check, root endpoint, and basic API functionality.

Author: Matthias Morath
Created: 2025-01-28
"""

# MARK: ━━━ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import logging
import pytest
from fastapi.testclient import TestClient

# MARK: ━━━ Logger ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logger = logging.getLogger(__name__)


# MARK: ━━━ Test Cases ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def test_root_endpoint(client: TestClient) -> None:
    """Test that the root endpoint returns a successful response."""
    logger.info("Testing root endpoint")

    response = client.get("/")

    assert response.status_code == 200, "Expected HTTP 200 OK"
    json_response = response.json()

    logger.debug("Root response: %s", json_response)
    assert json_response["status"] == "success"
    assert "Logistics Management System" in json_response["message"]
    assert "data" in json_response


def test_health_check(client: TestClient) -> None:
    """Test that the health check endpoint returns a successful response."""
    logger.info("Testing health check endpoint")

    response = client.get("/health")

    assert response.status_code == 200, "Expected HTTP 200 OK"
    json_response = response.json()

    logger.debug("Health check response: %s", json_response)
    assert json_response["status"] == "success"
    assert json_response["message"] == "System is healthy"
    assert json_response["data"]["status"] == "operational"


def test_api_documentation_available(client: TestClient) -> None:
    """Test that API documentation is available."""
    logger.info("Testing API documentation availability")

    # Test OpenAPI schema
    response = client.get("/openapi.json")
    assert response.status_code == 200, "OpenAPI schema should be available"

    # Test Swagger UI
    response = client.get("/docs")
    assert response.status_code == 200, "Swagger UI should be available"

    # Test ReDoc
    response = client.get("/redoc")
    assert response.status_code == 200, "ReDoc should be available"


# EOF
