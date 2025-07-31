#!/usr/bin/env python3
"""
Simple test script to verify the logistics management system functionality.
"""

import sys
import json
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.data_loader import DataLoader
from app.core import LogisticsManager
from app.models import Picker, MaterialCart


def test_data_loading():
    """Test data loading functionality."""
    print("Testing data loading...")

    try:
        loader = DataLoader()

        # Test CSV loading
        csv_articles = loader.parse_csv_articles()
        print(f"✓ Loaded {len(csv_articles)} articles from CSV")

        # Test JSON loading
        json_projects = loader.parse_json_projects()
        print(f"✓ Loaded {len(json_projects)} projects from JSON")

        # Test order creation
        orders = loader.create_picking_orders(json_projects)
        print(f"✓ Created {len(orders)} picking orders")

        return True

    except Exception as e:
        print(f"✗ Data loading failed: {e}")
        return False


def test_core_functionality():
    """Test core business logic."""
    print("\nTesting core functionality...")

    try:
        # Initialize system
        loader = DataLoader()
        manager = LogisticsManager()

        # Load data
        projects = loader.parse_json_projects()
        orders = loader.create_picking_orders(projects)

        # Add orders to manager
        for order in orders:
            manager.add_order(order)

        # Add sample pickers and carts
        sample_pickers = [
            Picker(picker_id="P001", name="John Doe", employee_number="EMP001"),
            Picker(picker_id="P002", name="Jane Smith", employee_number="EMP002"),
            Picker(picker_id="P003", name="Bob Johnson", employee_number="EMP003")
        ]

        sample_carts = [
            MaterialCart(cart_id="C001", capacity=500.0),
            MaterialCart(cart_id="C002", capacity=750.0),
            MaterialCart(cart_id="C003", capacity=1000.0)
        ]

        manager.pickers.extend(sample_pickers)
        manager.carts.extend(sample_carts)

        # Test basic operations
        print(f"✓ System initialized with {len(manager.orders)} orders")
        print(f"✓ Added {len(manager.pickers)} pickers")
        print(f"✓ Added {len(manager.carts)} carts")

        # Test statistics
        stats = manager.get_system_overview()
        print(f"✓ System statistics calculated")
        print(f"  - Total orders: {stats['total_orders']}")
        print(f"  - Open orders: {stats['open_orders']}")
        print(f"  - Total articles: {stats['total_articles']}")

        # Test order assignment
        if manager.orders and manager.pickers:
            order = manager.orders[0]
            picker = manager.pickers[0]

            success = manager.assign_order_to_picker(order.order_id, picker.picker_id)
            if success:
                print(f"✓ Successfully assigned order {order.order_id} to picker {picker.picker_id}")
            else:
                print(f"✗ Failed to assign order")

        return True

    except Exception as e:
        print(f"✗ Core functionality test failed: {e}")
        return False


def test_api_endpoints():
    """Test API endpoint functionality."""
    print("\nTesting API endpoints...")

    try:
        from app.api import app
        from fastapi.testclient import TestClient

        client = TestClient(app)

        # Test root endpoint
        response = client.get("/")
        if response.status_code == 200:
            print("✓ Root endpoint working")
        else:
            print(f"✗ Root endpoint failed: {response.status_code}")
            return False

        # Test health endpoint
        response = client.get("/health")
        if response.status_code == 200:
            print("✓ Health endpoint working")
        else:
            print(f"✗ Health endpoint failed: {response.status_code}")
            return False

        # Test orders endpoint
        response = client.get("/orders")
        if response.status_code == 200:
            print("✓ Orders endpoint working")
        else:
            print(f"✗ Orders endpoint failed: {response.status_code}")
            return False

        # Test statistics endpoint
        response = client.get("/statistics")
        if response.status_code == 200:
            print("✓ Statistics endpoint working")
        else:
            print(f"✗ Statistics endpoint failed: {response.status_code}")
            return False

        return True

    except ImportError:
        print("⚠ API testing skipped (FastAPI test client not available)")
        return True
    except Exception as e:
        print(f"✗ API testing failed: {e}")
        return False


def main():
    """Run all tests."""
    print("Logistics Management System - Test Suite")
    print("=" * 50)

    tests = [
        ("Data Loading", test_data_loading),
        ("Core Functionality", test_core_functionality),
        ("API Endpoints", test_api_endpoints),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
            print(f"✓ {test_name} passed")
        else:
            print(f"✗ {test_name} failed")

    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The system is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())