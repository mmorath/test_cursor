# File: backend/tests/test_data_loading.py
# Path: backend/tests/test_data_loading.py

"""
Test: Data Loading and Processing Tests
Description:
    Verifies that data can be loaded from CSV and JSON files correctly.
    Tests the data service functionality with real data files.

Author: Matthias Morath
Created: 2025-01-28
"""

# MARK: ━━━ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import logging

from app.services.data_service import DataService
from app.models import Article, Project

# MARK: ━━━ Logger ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logger = logging.getLogger(__name__)


# MARK: ━━━ Test Cases ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def test_data_service_initialization():
    """Test that DataService can be initialized correctly."""
    logger.info("Testing DataService initialization")

    data_service = DataService()
    assert data_service is not None
    assert hasattr(data_service, "data_dir")


def test_csv_data_loading():
    """Test loading data from CSV file."""
    logger.info("Testing CSV data loading")

    data_service = DataService()

    # Load raw CSV data
    raw_data = data_service.load_csv_data("orig.csv")
    assert len(raw_data) > 0, "Should load some data from CSV"

    logger.info(f"Loaded {len(raw_data)} records from CSV")

    # Check first record structure
    first_record = raw_data[0]
    assert "projekt_nr" in first_record
    assert "artikel" in first_record
    assert "menge" in first_record
    assert "lagerplatz" in first_record


def test_json_data_loading():
    """Test loading data from JSON file."""
    logger.info("Testing JSON data loading")

    data_service = DataService()

    # Load raw JSON data
    raw_data = data_service.load_json_data("project.json")
    assert "projects" in raw_data, "JSON should contain projects key"

    projects = raw_data["projects"]
    assert len(projects) > 0, "Should have at least one project"

    logger.info(f"Loaded {len(projects)} projects from JSON")

    # Check first project structure
    first_project = projects[0]
    assert "projekt_nr" in first_project
    assert "articles" in first_project


def test_csv_article_parsing():
    """Test parsing CSV data into Article objects."""
    logger.info("Testing CSV article parsing")

    data_service = DataService()

    # Parse CSV into Article objects
    articles = data_service.parse_csv_articles("orig.csv")
    assert len(articles) > 0, "Should parse some articles"

    logger.info(f"Parsed {len(articles)} articles from CSV")

    # Check first article
    first_article = articles[0]
    assert isinstance(first_article, Article)
    assert first_article.projekt_nr == "54536"
    assert first_article.artikel == "388303408"
    assert first_article.menge == 3
    assert first_article.lagerplatz == "23IZ022A"


def test_json_project_parsing():
    """Test parsing JSON data into Project objects."""
    logger.info("Testing JSON project parsing")

    data_service = DataService()

    # Parse JSON into Project objects
    projects = data_service.parse_json_projects("project.json")
    assert len(projects) > 0, "Should parse some projects"

    logger.info(f"Parsed {len(projects)} projects from JSON")

    # Check first project
    first_project = projects[0]
    assert isinstance(first_project, Project)
    assert first_project.projekt_nr == "054516"
    assert len(first_project.articles) > 0


def test_picking_order_creation():
    """Test creating picking orders from projects."""
    logger.info("Testing picking order creation")

    data_service = DataService()

    # Load and parse projects
    projects = data_service.parse_json_projects("project.json")

    # Create picking orders
    orders = data_service.create_picking_orders(projects)
    assert len(orders) > 0, "Should create some orders"

    logger.info(f"Created {len(orders)} picking orders")

    # Check first order
    first_order = orders[0]
    assert first_order.order_id.startswith("ORDER-")
    assert first_order.project.projekt_nr == "054516"
    assert first_order.status.value == "Offen"


def test_data_validation():
    """Test data validation and consistency checks."""
    logger.info("Testing data validation")

    data_service = DataService()

    # Load articles and validate
    articles = data_service.parse_csv_articles("orig.csv")
    validation_report = data_service.validate_data_consistency(articles)

    assert validation_report["total_articles"] > 0
    assert validation_report["valid_articles"] > 0

    logger.info(f"Validation report: {validation_report}")


# EOF
