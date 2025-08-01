# File: backend/tests/test_data_upload.py
# Path: backend/tests/test_data_upload.py

"""
Test: Data Upload API Tests
Description:
    Verifies that CSV files can be uploaded and processed via REST API.

Author: Matthias Morath
Created: 2025-01-28
"""

import pytest
import tempfile
import os
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_csv_content():
    """Sample CSV content for testing."""
    return """projekt_nr|abteilungsgruppe|kostenstelle|baugruppe|artikel|artikel_bezeichnung|menge|einheit|gewicht|lagerplatz|filter|bestand|wohin|lz|lager_1_stueckliste|lager_2_bedarfslager|lager_3_referenzen|status|position|bearbeitungsart|vorgang_id|anzahl_aktion
054536|LOGISTIK ALLES|2KF|919713008|388303408|SPANNPRATZE GS18NIMOCR36 FLZN|3|stk|,771|23IZ022A|23I|596|SHL-SHV--V01||MZS|MZS|SHL|Offen|578954208||127099|0
054536|LOGISTIK ALLES|2KF|919713008|451227008|BOLZEN DIN 1435 25X75X65 42CRMO4 GASN. SPF|1|stk|,33|23IZ123A|23I|640|SVR-SHV--V01||MZS|MZS|SVL|Offen|578954122||127099|0"""


def test_upload_csv_data(client, sample_csv_content):
    """Test uploading CSV data via REST API."""
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv", encoding="utf-8"
    ) as temp_file:
        temp_file.write(sample_csv_content)
        temp_file_path = temp_file.name

    try:
        # Upload the CSV file
        with open(temp_file_path, "rb") as csv_file:
            response = client.post(
                "/api/v1/data/upload/csv",
                files={"file": ("test.csv", csv_file, "text/csv")},
                data={"delimiter": "|", "skip_initial_space": "true"},
            )

        # Check response
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "CSV data uploaded and processed successfully" in data["message"]
        
        # Check response data
        response_data = data["data"]
        assert response_data["filename"] == "test.csv"
        assert response_data["total_records"] == 2
        assert response_data["articles_parsed"] == 2
        assert response_data["projects_created"] == 1
        assert response_data["orders_created"] == 1
        assert len(response_data["sample_articles"]) == 2

    finally:
        # Clean up temporary file
        os.unlink(temp_file_path)


def test_upload_invalid_file_type(client):
    """Test uploading non-CSV file."""
    # Create a temporary text file
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".txt", encoding="utf-8"
    ) as temp_file:
        temp_file.write("This is not a CSV file")
        temp_file_path = temp_file.name

    try:
        # Upload the text file
        with open(temp_file_path, "rb") as text_file:
            response = client.post(
                "/api/v1/data/upload/csv",
                files={"file": ("test.txt", text_file, "text/plain")},
            )

        # Check response
        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "error"
        assert "Invalid file type" in data["message"]

    finally:
        # Clean up temporary file
        os.unlink(temp_file_path)


def test_load_default_data(client):
    """Test loading default data via REST API."""
    response = client.post("/api/v1/data/load/default")
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Default data loaded successfully" in data["message"]


def test_get_data_status(client):
    """Test getting data status via REST API."""
    response = client.get("/api/v1/data/status")
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Data status retrieved successfully" in data["message"]
    
    # Check response data structure
    response_data = data["data"]
    assert "orders_count" in response_data
    assert "pickers_count" in response_data
    assert "carts_count" in response_data
    assert "open_orders" in response_data
    assert "in_progress_orders" in response_data
    assert "completed_orders" in response_data


# EOF 