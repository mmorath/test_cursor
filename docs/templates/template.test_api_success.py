# File: test_example.py
# Path: tests/api/test_example.py

"""
Test: Example API Success Test
Description:
    Verifies the success case of the /api/v1/example/validate route.
    Ensures the route responds with 200 OK and wraps data correctly.

Author: Matthias Morath
Created: 2025-07-24
"""

# MARK: ━━━ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import logging
import pytest
from fastapi.testclient import TestClient
from main import app

# MARK: ━━━ Logger ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logger = logging.getLogger(__name__)

# MARK: ━━━ TestClient Setup ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
client = TestClient(app)

# MARK: ━━━ Test Cases ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def test_validate_success() -> None:
    """Test that the /validate endpoint returns a successful response"""
    payload = {"input": "valid data"}

    logger.debug("Sending payload to /api/v1/example/validate: %s", payload)
    response = client.post("/api/v1/example/validate", json=payload)

    assert response.status_code == 200, "Expected HTTP 200 OK"
    json_response = response.json()

    logger.debug("Response: %s", json_response)
    assert json_response["success"] is True
    assert json_response["error"] is None
    assert "data" in json_response


# EOF
