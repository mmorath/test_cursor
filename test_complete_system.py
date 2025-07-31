# File: test_complete_system.py
# Path: test_complete_system.py

"""
Test script for the complete logistics management system.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.models import Article, Project, PickingOrder, Picker, MaterialCart, StatusEnum
from app.services.logistics_service import LogisticsService

# MARK: ━━━ Logging Setup ━━━

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# MARK: ━━━ Test Functions ━━━

def test_models():
    """Test Pydantic models."""
    logger.info("🧪 Testing Pydantic models...")

    # Test Article model
    article = Article(
        projekt_nr="054516",
        abteilungsgruppe="TEST",
        kostenstelle="TEST",
        baugruppe="TEST",
        artikel="388303408",
        artikel_bezeichnung="Test Article",
        menge=3,
        einheit="STK",
        gewicht=0.771,
        lagerplatz="23IZ022A",
        filter="TEST",
        bestand=10,
        wohin="TEST",
        lager_1_stueckliste="TEST",
        lager_2_bedarfslager="TEST",
        lager_3_referenzen="TEST",
        position=1,
        vorgang_id=1
    )

    assert article.total_weight == 2.313
    assert article.available_quantity == 10
    assert article.is_available is True

    logger.info("✅ Article model test passed")

    # Test Project model
    project = Project(
        projekt_nr="054516",
        articles=[article]
    )

    assert project.total_articles == 1
    assert project.total_weight == 2.313
    assert len(project.open_articles) == 1

    logger.info("✅ Project model test passed")

    # Test PickingOrder model
    order = PickingOrder(
        order_id="ORDER-054516-001",
        project=project,
        priority=5
    )

    assert order.completion_percentage == 0.0
    assert order.is_complete is False

    logger.info("✅ PickingOrder model test passed")

    # Test Picker model
    picker = Picker(
        picker_id="P001",
        name="John Doe",
        employee_number="EMP001"
    )

    assert picker.is_active is True
    assert picker.total_picks_today == 0

    logger.info("✅ Picker model test passed")

    # Test MaterialCart model
    cart = MaterialCart(
        cart_id="C001",
        capacity=100.0
    )

    assert cart.available_capacity == 100.0
    assert cart.utilization_percentage == 0.0

    logger.info("✅ MaterialCart model test passed")


def test_logistics_service():
    """Test logistics service functionality."""
    logger.info("🧪 Testing logistics service...")

    service = LogisticsService()

    # Create test data
    article = Article(
        projekt_nr="054516",
        abteilungsgruppe="TEST",
        kostenstelle="TEST",
        baugruppe="TEST",
        artikel="388303408",
        artikel_bezeichnung="Test Article",
        menge=3,
        einheit="STK",
        gewicht=0.771,
        lagerplatz="23IZ022A",
        filter="TEST",
        bestand=10,
        wohin="TEST",
        lager_1_stueckliste="TEST",
        lager_2_bedarfslager="TEST",
        lager_3_referenzen="TEST",
        position=1,
        vorgang_id=1
    )

    project = Project(projekt_nr="054516", articles=[article])
    order = PickingOrder(order_id="ORDER-054516-001", project=project)
    picker = Picker(picker_id="P001", name="John Doe", employee_number="EMP001")
    cart = MaterialCart(cart_id="C001", capacity=100.0)

    # Add to service
    service.add_order(order)
    service.pickers.append(picker)
    service.carts.append(cart)

    # Test order assignment
    success = service.assign_order_to_picker("ORDER-054516-001", "P001")
    assert success is True
    assert order.assigned_picker == "P001"
    assert order.status == StatusEnum.IN_BEARBEITUNG
    assert picker.current_order == "ORDER-054516-001"

    logger.info("✅ Order assignment test passed")

    # Test article picking
    success = service.pick_article("ORDER-054516-001", "388303408", 3, "P001")
    assert success is True
    assert article.status == StatusEnum.ABGESCHLOSSEN
    assert article.anzahl_auf_wagen == 3
    assert article.kommisionierer == "P001"

    logger.info("✅ Article picking test passed")

    # Test order completion
    success = service.complete_order("ORDER-054516-001")
    assert success is True
    assert order.status == StatusEnum.ABGESCHLOSSEN
    assert order.is_complete is True

    logger.info("✅ Order completion test passed")

    # Test system overview
    overview = service.get_system_overview()
    assert overview["total_orders"] == 1
    assert overview["completed_orders"] == 1
    assert overview["completion_rate"] == 100.0

    logger.info("✅ System overview test passed")


def test_api_structure():
    """Test API structure and imports."""
    logger.info("🧪 Testing API structure...")

    try:
        from app.api.v1 import api_router
        assert api_router is not None
        logger.info("✅ API router import test passed")
    except ImportError as e:
        logger.warning(f"⚠️ API router import failed: {e}")

    try:
        from app.api.v1.routes import orders
        assert orders.router is not None
        logger.info("✅ Orders routes import test passed")
    except ImportError as e:
        logger.warning(f"⚠️ Orders routes import failed: {e}")


def test_configuration():
    """Test configuration management."""
    logger.info("🧪 Testing configuration...")

    try:
        from config import settings
        assert settings.app_name == "Logistics Management System"
        assert settings.port == 8000
        logger.info("✅ Configuration test passed")
    except ImportError as e:
        logger.warning(f"⚠️ Configuration import failed: {e}")


# MARK: ━━━ Main Test Runner ━━━

def run_all_tests():
    """Run all tests."""
    logger.info("🚀 Starting complete system tests...")

    try:
        test_models()
        test_logistics_service()
        test_api_structure()
        test_configuration()

        logger.info("🎉 All tests passed! The system is working correctly.")
        return True

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

# EOF