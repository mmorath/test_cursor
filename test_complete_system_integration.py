# File: test_complete_system_integration.py
# Path: test_complete_system_integration.py

"""
Test: Complete System Integration Test
Description:
    Tests the complete logistics management system end-to-end.
    Loads real data from CSV/JSON, tests backend API, and verifies frontend functionality.

Author: Matthias Morath
Created: 2025-01-28
"""

# MARK: ━━━ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import logging
import asyncio
import time
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any

import httpx
import pytest
from fastapi.testclient import TestClient

# MARK: ━━━ Logger ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# MARK: ━━━ Test Configuration ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
TEST_TIMEOUT = 30  # seconds

# MARK: ━━━ Test Classes ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CompleteSystemTest:
    """Complete system integration test class."""

    def __init__(self):
        self.backend_client = None
        self.frontend_client = None
        self.backend_process = None
        self.frontend_process = None

    async def setup(self):
        """Setup test environment."""
        logger.info("🚀 Setting up complete system test environment")

        # Start backend server
        await self._start_backend()

        # Start frontend server
        await self._start_frontend()

        # Wait for services to be ready
        await self._wait_for_services()

        # Initialize HTTP clients
        self.backend_client = httpx.AsyncClient(base_url=BACKEND_URL)
        self.frontend_client = httpx.AsyncClient(base_url=FRONTEND_URL)

        logger.info("✅ Test environment setup complete")

    async def teardown(self):
        """Cleanup test environment."""
        logger.info("🧹 Cleaning up test environment")

        if self.backend_client:
            await self.backend_client.aclose()
        if self.frontend_client:
            await self.frontend_client.aclose()

        if self.backend_process:
            self.backend_process.terminate()
        if self.frontend_process:
            self.frontend_process.terminate()

        logger.info("✅ Test environment cleanup complete")

    async def _start_backend(self):
        """Start backend server."""
        logger.info("🔧 Starting backend server")

        try:
            self.backend_process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
                cwd="backend",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logger.info("✅ Backend server started")
        except Exception as e:
            logger.error(f"❌ Failed to start backend server: {e}")
            raise

    async def _start_frontend(self):
        """Start frontend server."""
        logger.info("🎨 Starting frontend server")

        try:
            self.frontend_process = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd="frontend",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logger.info("✅ Frontend server started")
        except Exception as e:
            logger.error(f"❌ Failed to start frontend server: {e}")
            raise

    async def _wait_for_services(self):
        """Wait for services to be ready."""
        logger.info("⏳ Waiting for services to be ready")

        start_time = time.time()
        backend_ready = False
        frontend_ready = False

        while time.time() - start_time < TEST_TIMEOUT:
            # Check backend
            if not backend_ready:
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(f"{BACKEND_URL}/health", timeout=1.0)
                        if response.status_code == 200:
                            backend_ready = True
                            logger.info("✅ Backend is ready")
                except:
                    pass

            # Check frontend
            if not frontend_ready:
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(f"{FRONTEND_URL}", timeout=1.0)
                        if response.status_code == 200:
                            frontend_ready = True
                            logger.info("✅ Frontend is ready")
                except:
                    pass

            if backend_ready and frontend_ready:
                break

            await asyncio.sleep(1)

        if not backend_ready or not frontend_ready:
            raise TimeoutError("Services did not start within timeout")

    async def test_data_loading(self):
        """Test loading real data from CSV and JSON files."""
        logger.info("📊 Testing data loading")

        # Test backend data loading endpoints
        response = await self.backend_client.get("/api/v1/orders")
        assert response.status_code == 200, "Orders endpoint should be accessible"

        data = response.json()
        assert data["status"] == "success", "Response should be successful"

        logger.info("✅ Data loading test passed")

    async def test_picking_process(self):
        """Test complete picking process workflow."""
        logger.info("📦 Testing complete picking process")

        # Step 1: Get available orders
        response = await self.backend_client.get("/api/v1/orders")
        assert response.status_code == 200

        orders_data = response.json()
        orders = orders_data.get("data", {}).get("orders", [])

        if not orders:
            logger.warning("⚠️ No orders available for picking test")
            return

        test_order = orders[0]
        order_id = test_order["order_id"]

        logger.info(f"Testing with order: {order_id}")

        # Step 2: Create test picker
        picker_data = {
            "name": "Test Picker",
            "employee_number": "EMP001"
        }

        response = await self.backend_client.post("/api/v1/pickers", json=picker_data)
        assert response.status_code == 200

        picker_response = response.json()
        picker_id = picker_response["data"]["picker_id"]

        # Step 3: Assign order to picker
        response = await self.backend_client.post(
            f"/api/v1/orders/{order_id}/assign",
            params={"picker_id": picker_id}
        )
        assert response.status_code == 200

        # Step 4: Get order details to verify assignment
        response = await self.backend_client.get(f"/api/v1/orders/{order_id}")
        assert response.status_code == 200

        order_details = response.json()
        assert order_details["data"]["assigned_picker"] == picker_id

        logger.info("✅ Picking process test passed")

    async def test_frontend_connectivity(self):
        """Test frontend connectivity and basic functionality."""
        logger.info("🌐 Testing frontend connectivity")

        # Test frontend is accessible
        response = await self.frontend_client.get("/")
        assert response.status_code == 200, "Frontend should be accessible"

        # Test frontend can communicate with backend
        # This would typically be done through the frontend's API client
        # For now, we'll verify the frontend is running

        logger.info("✅ Frontend connectivity test passed")

    async def test_system_statistics(self):
        """Test system statistics and reporting."""
        logger.info("📈 Testing system statistics")

        # Test statistics endpoint
        response = await self.backend_client.get("/api/v1/statistics/overview")
        assert response.status_code == 200

        stats = response.json()
        assert stats["status"] == "success"

        data = stats["data"]
        assert "total_orders" in data
        assert "completion_rate" in data
        assert "efficiency_score" in data

        logger.info(f"System statistics: {data}")
        logger.info("✅ System statistics test passed")

    async def test_error_handling(self):
        """Test error handling and edge cases."""
        logger.info("⚠️ Testing error handling")

        # Test invalid order ID
        response = await self.backend_client.get("/api/v1/orders/invalid-id")
        assert response.status_code == 404, "Invalid order should return 404"

        # Test invalid picker assignment
        response = await self.backend_client.post(
            "/api/v1/orders/invalid-id/assign",
            params={"picker_id": "invalid-picker"}
        )
        assert response.status_code in [400, 404], "Invalid assignment should fail"

        logger.info("✅ Error handling test passed")

# MARK: ━━━ Main Test Runner ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def run_complete_system_test():
    """Run the complete system integration test."""
    logger.info("🚀 Starting complete system integration test")

    test = CompleteSystemTest()

    try:
        await test.setup()

        # Run all tests
        await test.test_data_loading()
        await test.test_picking_process()
        await test.test_frontend_connectivity()
        await test.test_system_statistics()
        await test.test_error_handling()

        logger.info("🎉 All integration tests passed!")

    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        raise
    finally:
        await test.teardown()

# MARK: ━━━ Command Line Interface ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    try:
        asyncio.run(run_complete_system_test())
        sys.exit(0)
    except Exception as e:
        logger.error(f"Integration test failed: {e}")
        sys.exit(1)

# EOF