# File: Makefile
# Path: Makefile
# Description: Makefile for Logistics Management System
# Provides commands for testing, development, and deployment.

# MARK: ━━━ Variables ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PYTHON = python3
PIP = pip3
PYTEST = pytest
BACKEND_DIR = backend
FRONTEND_DIR = frontend
TEST_DIR = tests

# MARK: ━━━ Development Commands ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.PHONY: install
install:
	@echo "📦 Installing dependencies..."
	cd $(BACKEND_DIR) && $(PIP) install -r requirements.txt
	cd $(FRONTEND_DIR) && $(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed"

.PHONY: install-dev
install-dev:
	@echo "📦 Installing development dependencies..."
	$(PIP) install pytest pytest-cov pytest-asyncio httpx black flake8 mypy bandit
	@echo "✅ Development dependencies installed"

# MARK: ━━━ Testing Commands ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.PHONY: test
test: test-backend test-frontend test-integration
	@echo "🎉 All tests completed!"

.PHONY: test-backend
test-backend:
	@echo "🧪 Running backend tests..."
	cd $(BACKEND_DIR) && $(PYTEST)
	@echo "✅ Backend tests completed"

.PHONY: test-frontend
test-frontend:
	@echo "🎨 Running frontend tests..."
	cd $(FRONTEND_DIR) && $(PYTEST) --tb=short
	@echo "✅ Frontend tests completed"

.PHONY: test-integration
test-integration:
	@echo "🔗 Running integration tests..."
	$(PYTHON) test_complete_system_integration.py
	@echo "✅ Integration tests completed"

.PHONY: test-quick
test-quick:
	@echo "⚡ Running quick tests..."
	cd $(BACKEND_DIR) && $(PYTEST) -x --tb=short
	cd $(FRONTEND_DIR) && $(PYTEST) -x --tb=short
	@echo "✅ Quick tests completed"

# MARK: ━━━ Code Quality Commands ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.PHONY: lint
lint:
	@echo "🔍 Running linting checks..."
	flake8 $(BACKEND_DIR) $(FRONTEND_DIR) --max-line-length=79 --extend-ignore=E203,W503
	@echo "✅ Linting completed"

.PHONY: format
format:
	@echo "🎨 Formatting code..."
	black $(BACKEND_DIR) $(FRONTEND_DIR)
	@echo "✅ Code formatting completed"

.PHONY: format-check
format-check:
	@echo "🔍 Checking code formatting..."
	black --check $(BACKEND_DIR) $(FRONTEND_DIR)
	@echo "✅ Code formatting check completed"

.PHONY: type-check
type-check:
	@echo "🔍 Running type checks..."
	mypy $(BACKEND_DIR) $(FRONTEND_DIR) --ignore-missing-imports
	@echo "✅ Type checking completed"

.PHONY: security
security:
	@echo "🔒 Running security scan..."
	bandit -r $(BACKEND_DIR) -f json -o bandit-report.json
	@echo "✅ Security scan completed"

.PHONY: quality
quality: lint format-check type-check security
	@echo "✅ All quality checks completed"

# MARK: ━━━ Server Commands ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.PHONY: run-backend
run-backend:
	@echo "🔧 Starting backend server..."
	cd $(BACKEND_DIR) && $(PYTHON) -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

.PHONY: run-frontend
run-frontend:
	@echo "🎨 Starting frontend server..."
	cd $(FRONTEND_DIR) && $(PYTHON) main.py

.PHONY: run
run:
	@echo "🚀 Starting both servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "Press Ctrl+C to stop"
	@trap 'kill %1 %2' SIGINT; \
	$(MAKE) run-backend & \
	$(MAKE) run-frontend & \
	wait

# MARK: ━━━ Data Commands ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.PHONY: load-data
load-data:
	@echo "📊 Loading test data..."
	$(PYTHON) scripts/load_test_data.py
	@echo "✅ Test data loaded"

.PHONY: validate-data
validate-data:
	@echo "🔍 Validating data files..."
	$(PYTHON) scripts/validate_data.py
	@echo "✅ Data validation completed"

# MARK: ━━━ Cleanup Commands ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.PHONY: clean
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf $(BACKEND_DIR)/htmlcov
	rm -rf $(BACKEND_DIR)/.coverage
	rm -rf $(FRONTEND_DIR)/htmlcov
	rm -rf $(FRONTEND_DIR)/.coverage
	rm -f bandit-report.json
	@echo "✅ Cleanup completed"

.PHONY: clean-all
clean-all: clean
	@echo "🧹 Deep cleaning..."
	rm -rf $(BACKEND_DIR)/.venv
	rm -rf $(FRONTEND_DIR)/.venv
	@echo "✅ Deep cleanup completed"

# MARK: ━━━ Documentation Commands ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.PHONY: docs
docs:
	@echo "📚 Building documentation..."
	mkdocs build
	@echo "✅ Documentation built"

.PHONY: docs-serve
docs-serve:
	@echo "📚 Serving documentation..."
	mkdocs serve

# MARK: ━━━ Help ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.PHONY: help
help:
	@echo "🚀 Logistics Management System - Makefile"
	@echo ""
	@echo "Development:"
	@echo "  install        Install all dependencies"
	@echo "  install-dev    Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test           Run all tests"
	@echo "  test-backend   Run backend tests only"
	@echo "  test-frontend  Run frontend tests only"
	@echo "  test-integration Run integration tests"
	@echo "  test-quick     Run quick tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint           Run linting checks"
	@echo "  format         Format code with black"
	@echo "  format-check   Check code formatting"
	@echo "  type-check     Run type checking"
	@echo "  security       Run security scan"
	@echo "  quality        Run all quality checks"
	@echo ""
	@echo "Servers:"
	@echo "  run-backend    Start backend server"
	@echo "  run-frontend   Start frontend server"
	@echo "  run            Start both servers"
	@echo ""
	@echo "Data:"
	@echo "  load-data      Load test data"
	@echo "  validate-data  Validate data files"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean          Clean temporary files"
	@echo "  clean-all      Deep cleanup"
	@echo ""
	@echo "Documentation:"
	@echo "  docs           Build documentation"
	@echo "  docs-serve     Serve documentation"

# EOF
