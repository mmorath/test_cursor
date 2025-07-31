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

# Virtual environment paths
BACKEND_VENV = $(BACKEND_DIR)/.venv
FRONTEND_VENV = $(FRONTEND_DIR)/.venv

# Virtual environment executables
BACKEND_PYTHON = $(BACKEND_VENV)/bin/python
FRONTEND_PYTHON = $(FRONTEND_VENV)/bin/python
BACKEND_PIP = $(BACKEND_VENV)/bin/pip
FRONTEND_PIP = $(FRONTEND_VENV)/bin/pip
BACKEND_PYTEST = $(BACKEND_VENV)/bin/pytest
FRONTEND_PYTEST = $(FRONTEND_VENV)/bin/pytest

# MARK: ━━━ Development Commands ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.PHONY: install
install: setup-environments
	@echo "📦 Installing dependencies..."
	cd $(BACKEND_DIR) && .venv/bin/pip install -r requirements.txt
	cd $(FRONTEND_DIR) && .venv/bin/pip install -r requirements.txt
	@echo "✅ Dependencies installed"

.PHONY: setup-environments
setup-environments:
	@echo "🔧 Setting up virtual environments..."
	@if [ ! -d "$(BACKEND_VENV)" ]; then \
		echo "📦 Creating backend virtual environment..."; \
		cd $(BACKEND_DIR) && $(PYTHON) -m venv .venv; \
	fi
	@if [ ! -d "$(FRONTEND_VENV)" ]; then \
		echo "📦 Creating frontend virtual environment..."; \
		cd $(FRONTEND_DIR) && $(PYTHON) -m venv .venv; \
	fi
	@echo "✅ Virtual environments ready"

.PHONY: activate-backend
activate-backend:
	@echo "🔧 To activate backend environment, run:"
	@echo "   cd $(BACKEND_DIR) && source .venv/bin/activate"

.PHONY: activate-frontend
activate-frontend:
	@echo "🔧 To activate frontend environment, run:"
	@echo "   cd $(FRONTEND_DIR) && source .venv/bin/activate"

.PHONY: compile-requirements
compile-requirements: setup-environments
	@echo "🔧 Compiling requirements from .in files..."
	cd $(BACKEND_DIR) && .venv/bin/pip install pip-tools && .venv/bin/pip-compile requirements.in
	cd $(FRONTEND_DIR) && .venv/bin/pip install pip-tools && .venv/bin/pip-compile requirements.in
	@echo "✅ Requirements compiled"

.PHONY: update-requirements
update-requirements: setup-environments
	@echo "🔄 Updating requirements..."
	cd $(BACKEND_DIR) && $(BACKEND_PIP) install pip-tools && pip-compile --upgrade requirements.in
	cd $(FRONTEND_DIR) && $(FRONTEND_PIP) install pip-tools && pip-compile --upgrade requirements.in
	@echo "✅ Requirements updated"

.PHONY: install-dev
install-dev: setup-environments
	@echo "📦 Installing development dependencies..."
	cd $(BACKEND_DIR) && .venv/bin/pip install pytest pytest-cov pytest-asyncio httpx black flake8 mypy bandit
	cd $(FRONTEND_DIR) && .venv/bin/pip install pytest pytest-cov pytest-asyncio httpx black flake8 mypy bandit
	@echo "✅ Development dependencies installed"

# MARK: ━━━ Testing Commands ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.PHONY: test
test: test-backend test-frontend test-integration
	@echo "🎉 All tests completed!"

.PHONY: test-backend
test-backend: install
	@echo "🧪 Running backend tests..."
	cd $(BACKEND_DIR) && .venv/bin/pytest
	@echo "✅ Backend tests completed"

.PHONY: test-frontend
test-frontend: install
	@echo "🎨 Running frontend tests..."
	cd $(FRONTEND_DIR) && .venv/bin/pytest --tb=short
	@echo "✅ Frontend tests completed"

.PHONY: test-integration
test-integration:
	@echo "🔗 Running integration tests..."
	$(PYTHON) test_complete_system_integration.py
	@echo "✅ Integration tests completed"

.PHONY: test-quick
test-quick: install
	@echo "⚡ Running quick tests..."
	cd $(BACKEND_DIR) && .venv/bin/pytest -x --tb=short
	cd $(FRONTEND_DIR) && .venv/bin/pytest -x --tb=short
	@echo "✅ Quick tests completed"

# MARK: ━━━ Code Quality Commands ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.PHONY: lint
lint:
	@echo "🔍 Running linting checks..."
	flake8 $(BACKEND_DIR) $(FRONTEND_DIR) --max-line-length=79 --extend-ignore=E203,W503 --exclude=.venv,__pycache__,.git
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
run-backend: install
	@echo "🔧 Starting backend server..."
	cd $(BACKEND_DIR) && .venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

.PHONY: run-frontend
run-frontend: install
	@echo "🎨 Starting frontend server..."
	cd $(FRONTEND_DIR) && $(FRONTEND_PYTHON) main.py

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
	rm -rf .pytest_cache
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
	@echo "  setup-environments Create virtual environments"
	@echo "  compile-requirements Compile requirements from .in files"
	@echo "  update-requirements Update requirements to latest versions"
	@echo "  activate-backend Show backend activation command"
	@echo "  activate-frontend Show frontend activation command"
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
