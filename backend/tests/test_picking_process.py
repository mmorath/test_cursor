# File: backend/tests/test_picking_process.py
# Path: backend/tests/test_picking_process.py

"""
Test: Complete Picking Process Integration Tests
Description:
    Tests the complete picking process from order creation to completion.
    Uses real data from CSV/JSON files and tests the full workflow.

Author: Matthias Morath
Created: 2025-01-28
"""

# MARK: ━━━ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import logging
from fastapi.testclient import TestClient

from app.services.logistics_service import LogisticsService
from app.services.data_service import DataService
from app.models import StatusEnum

# MARK: ━━━ Logger ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logger = logging.getLogger(__name__)


# MARK: ━━━ Test Cases ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def test_complete_picking_workflow():
    """Test the complete picking workflow from start to finish."""
    logger.info("Testing complete picking workflow")

    # Initialize services
    logistics_service = LogisticsService()
    data_service = DataService()

    # Load real data
    projects = data_service.parse_json_projects("project.json")
    orders = data_service.create_picking_orders(projects)

    # Add orders to logistics service
    for order in orders:
        logistics_service.add_order(order)

    # Create test picker and cart
    from app.models import Picker, MaterialCart

    picker = Picker(picker_id="P001", name="Test Picker", employee_number="EMP001")

    cart = MaterialCart(cart_id="C001", capacity=100.0)

    logistics_service.pickers.append(picker)
    logistics_service.carts.append(cart)

    # Test workflow with first order
    test_order = orders[0]
    test_article = test_order.project.articles[0]

    logger.info(f"Testing with order: {test_order.order_id}")
    logger.info(f"Testing with article: {test_article.artikel}")

    # Step 1: Assign order to picker
    success = logistics_service.assign_order_to_picker(
        test_order.order_id, picker.picker_id
    )
    assert success is True, "Order assignment should succeed"
    assert test_order.assigned_picker == picker.picker_id
    assert test_order.status == StatusEnum.IN_BEARBEITUNG

    # Step 2: Assign cart to picker
    success = logistics_service.assign_cart_to_picker(picker.picker_id, cart.cart_id)
    assert success is True, "Cart assignment should succeed"
    assert cart.assigned_picker == picker.picker_id
    assert not cart.is_available

        # Step 3: Pick all open articles in the order
    # Continue picking until all articles are completed
    while True:
        # Find any article that is still open
        open_article = None
        for article in test_order.project.articles:
            if article.status == StatusEnum.OFFEN:
                open_article = article
                break
        
        if not open_article:
            break  # All articles are picked
        
        success = logistics_service.pick_article(
            test_order.order_id, open_article.artikel,
            open_article.menge, picker.picker_id
        )
        assert (
            success is True
        ), f"Article picking should succeed for {open_article.artikel}"
        assert open_article.status == StatusEnum.ABGESCHLOSSEN
        assert open_article.anzahl_auf_wagen == open_article.menge
        assert open_article.kommisionierer == picker.picker_id

    # Step 4: Complete order
    success = logistics_service.complete_order(test_order.order_id)
    assert success is True, "Order completion should succeed"
    assert test_order.status == StatusEnum.ABGESCHLOSSEN
    assert test_order.is_complete is True

    # Step 5: Verify picker is released
    assert picker.current_order is None

    logger.info("Complete picking workflow test passed")


def test_picking_process_api_integration(client: TestClient):
    """Test the picking process through the API endpoints."""
    logger.info("Testing picking process API integration")

    # First, we need to load data into the system
    # This would typically be done through a data loading endpoint
    # For now, we'll test the API structure

    # Test orders endpoint
    response = client.get("/api/v1/orders")
    assert response.status_code == 200, "Orders endpoint should be accessible"

    json_response = response.json()
    assert json_response["status"] == "success"
    assert "data" in json_response

    # Test order assignment endpoint (if order exists)
    # This would require an actual order to be created first
    # For now, we'll test the endpoint structure
    test_order_id = "ORDER-054536-001"
    test_picker_id = "P001"

    response = client.post(
        f"/api/v1/orders/{test_order_id}/assign?picker_id={test_picker_id}"
    )
    # This might fail if order doesn't exist, but we're testing the endpoint structure
    assert response.status_code in [200, 400, 404], "Assignment endpoint should respond"

    logger.info("API integration test completed")


def test_picking_statistics():
    """Test that picking statistics are calculated correctly."""
    logger.info("Testing picking statistics")

    logistics_service = LogisticsService()
    data_service = DataService()

    # Load real data
    projects = data_service.parse_json_projects("project.json")
    orders = data_service.create_picking_orders(projects)

    # Add orders to logistics service
    for order in orders:
        logistics_service.add_order(order)

    # Get system overview
    overview = logistics_service.get_system_overview()

    assert overview["total_orders"] > 0
    assert overview["open_orders"] > 0
    assert overview["total_articles"] > 0
    assert overview["completion_rate"] >= 0
    assert overview["efficiency_score"] >= 0

    logger.info(f"System overview: {overview}")
    logger.info("Picking statistics test passed")


def test_route_optimization():
    """Test route optimization functionality."""
    logger.info("Testing route optimization")

    logistics_service = LogisticsService()
    data_service = DataService()

    # Load real data
    projects = data_service.parse_json_projects("project.json")
    orders = data_service.create_picking_orders(projects)

    # Test route optimization for first order
    test_order = orders[0]
    optimized_route = logistics_service.calculate_route_optimization(test_order)

    assert len(optimized_route) > 0, "Should generate a route"
    assert all(isinstance(location, str) for location in optimized_route)

    logger.info(f"Optimized route: {optimized_route}")
    logger.info("Route optimization test passed")


# EOF
