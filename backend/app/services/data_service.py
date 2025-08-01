# File: backend/app/services/data_service.py
# Path: backend/app/services/data_service.py

"""
Data loading and validation service.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

from ..models import Article, Project, PickingOrder

logger = logging.getLogger(__name__)


class DataService:
    """Service for data loading and validation."""

    def __init__(self, data_dir: str = "../docs/data"):
        """Initialize data service with data directory."""
        self.data_dir = Path(data_dir)
        self._validate_data_directory()

    def _validate_data_directory(self) -> None:
        """Validate that data directory exists."""
        if not self.data_dir.exists():
            raise FileNotFoundError(
                f"Data directory not found: {self.data_dir}"
            )
        if not self.data_dir.is_dir():
            raise NotADirectoryError(
                f"Path is not a directory: {self.data_dir}"
            )

    def load_csv_data(
        self, filename: str = "orig.csv"
    ) -> List[Dict[str, Any]]:
        """Load data from CSV file."""
        file_path = self.data_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        try:
            logger.info(f"Loading CSV data from {filename}")
            df = pd.read_csv(file_path, sep="|", skipinitialspace=True)
            df.columns = df.columns.str.strip()
            data = df.to_dict("records")
            logger.info(f"Loaded {len(data)} records from {filename}")
            return data
        except Exception as e:
            logger.error(f"Error loading CSV file {filename}: {e}")
            raise

    def load_json_data(self, filename: str = "project.json") -> Dict[str, Any]:
        """Load data from JSON file."""
        file_path = self.data_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {file_path}")

        try:
            logger.info(f"Loading JSON data from {filename}")
            with open(file_path, "r", encoding="utf-8") as f:
                import json

                data = json.load(f)
            logger.info(f"Loaded JSON data from {filename}")
            return data
        except Exception as e:
            logger.error(f"Error loading JSON file {filename}: {e}")
            raise

    def parse_csv_articles(self, filename: str = "orig.csv") -> List[Article]:
        """Parse CSV data into Article objects."""
        raw_data = self.load_csv_data(filename)
        articles = []

        for row in raw_data:
            try:
                cleaned_row = self._clean_row_data(row)
                article = Article(**cleaned_row)
                articles.append(article)
            except Exception as e:
                logger.warning(f"Failed to parse row: {e}")
                continue

        logger.info(f"Successfully parsed {len(articles)} articles from CSV")
        return articles

    def parse_json_projects(
        self, filename: str = "project.json"
    ) -> List[Project]:
        """Parse JSON data into Project objects."""
        raw_data = self.load_json_data(filename)
        projects = []

        for project_data in raw_data.get("projects", []):
            try:
                project = self._create_project_from_data(project_data)
                projects.append(project)
            except Exception as e:
                logger.warning(f"Failed to parse project: {e}")
                continue

        logger.info(f"Successfully parsed {len(projects)} projects from JSON")
        return projects

    def _clean_row_data(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and convert row data for Article creation."""
        cleaned = {}

        # Handle weight conversion (comma to dot)
        if "gewicht" in row:
            weight_str = str(row["gewicht"]).replace(",", ".")
            try:
                cleaned["gewicht"] = float(weight_str)
            except ValueError:
                cleaned["gewicht"] = 0.0

        # Handle numeric fields
        numeric_fields = [
            "menge",
            "bestand",
            "position",
            "vorgang_id",
            "anzahl_aktion",
        ]
        for field in numeric_fields:
            if field in row:
                try:
                    cleaned[field] = int(str(row[field]).strip())
                except (ValueError, TypeError):
                    cleaned[field] = 0

        # Handle optional fields
        optional_fields = [
            "anzahl_auf_wagen",
            "anzahl_fehlt",
            "anzahl_beschaedigt",
        ]
        for field in optional_fields:
            if field in row and row[field]:
                try:
                    cleaned[field] = int(str(row[field]).strip())
                except (ValueError, TypeError):
                    cleaned[field] = None
            else:
                cleaned[field] = None

        # Handle string fields
        string_fields = [
            "projekt_nr",
            "abteilungsgruppe",
            "kostenstelle",
            "baugruppe",
            "artikel",
            "artikel_bezeichnung",
            "einheit",
            "lagerplatz",
            "filter",
            "wohin",
            "lz",
            "lager_1_stueckliste",
            "lager_2_bedarfslager",
            "lager_3_referenzen",
            "status",
            "bearbeitungsart",
            "kommisionierer",
            "materialwagen",
        ]

        for field in string_fields:
            if field in row:
                cleaned[field] = str(row[field]).strip()
            else:
                cleaned[field] = ""

        return cleaned

    def _create_project_from_data(
        self, project_data: Dict[str, Any]
    ) -> Project:
        """Create Project object from project data."""
        articles = []

        for article_data in project_data.get("articles", []):
            try:
                article = Article(**article_data)
                articles.append(article)
            except Exception as e:
                logger.warning(f"Failed to parse article in project: {e}")
                continue

        return Project(
            projekt_nr=project_data["projekt_nr"], articles=articles
        )

    def create_picking_orders(
        self, projects: List[Project]
    ) -> List[PickingOrder]:
        """Create picking orders from projects."""
        orders = []

        for i, project in enumerate(projects):
            order_id = f"ORDER-{project.projekt_nr}-{i+1:03d}"

            order = PickingOrder(
                order_id=order_id,
                project=project,
                priority=self._calculate_priority(project),
            )

            orders.append(order)

        logger.info(f"Created {len(orders)} picking orders")
        return orders

    def _calculate_priority(self, project: Project) -> int:
        """Calculate priority based on project characteristics."""
        weight_factor = min(project.total_weight / 100, 5)
        article_factor = min(project.total_articles / 10, 3)

        priority = int(weight_factor + article_factor + 1)
        return min(priority, 10)

    def validate_data_consistency(
        self, articles: List[Article]
    ) -> Dict[str, Any]:
        """Validate data consistency and return validation report."""
        report = {
            "total_articles": len(articles),
            "valid_articles": 0,
            "invalid_articles": 0,
            "missing_stock": 0,
            "weight_issues": 0,
            "status_distribution": {},
            "project_distribution": {},
        }

        for article in articles:
            # Articles are already validated when created
            report["valid_articles"] += 1

            if not article.is_available:
                report["missing_stock"] += 1

            if article.gewicht <= 0:
                report["weight_issues"] += 1

            status = article.status.value
            report["status_distribution"][status] = (
                report["status_distribution"].get(status, 0) + 1
            )

            project = article.projekt_nr
            report["project_distribution"][project] = (
                report["project_distribution"].get(project, 0) + 1
            )

        logger.info(f"Data validation completed: {report}")
        return report

    def _load_csv_from_path(
        self, file_path: str, delimiter: str = "|", skip_initial_space: bool = True
    ) -> List[Dict[str, Any]]:
        """Load data from CSV file at specific path."""
        try:
            logger.info(f"Loading CSV data from {file_path}")
            df = pd.read_csv(file_path, sep=delimiter, skipinitialspace=skip_initial_space)
            df.columns = df.columns.str.strip()
            data = df.to_dict("records")
            logger.info(f"Loaded {len(data)} records from {file_path}")
            return data
        except Exception as e:
            logger.error(f"Error loading CSV file {file_path}: {e}")
            raise

    def _parse_csv_articles_from_data(self, raw_data: List[Dict[str, Any]]) -> List[Article]:
        """Parse raw CSV data into Article objects."""
        articles = []

        for row in raw_data:
            try:
                cleaned_row = self._clean_row_data(row)
                article = Article(**cleaned_row)
                articles.append(article)
            except Exception as e:
                logger.warning(f"Failed to parse row: {e}")
                continue

        logger.info(f"Successfully parsed {len(articles)} articles from CSV data")
        return articles

    def _create_projects_from_articles(self, articles: List[Article]) -> List[Project]:
        """Create projects from articles by grouping by project number."""
        from collections import defaultdict
        
        # Group articles by project number
        project_groups = defaultdict(list)
        for article in articles:
            project_groups[article.projekt_nr].append(article)
        
        # Create projects
        projects = []
        for projekt_nr, project_articles in project_groups.items():
            project = Project(projekt_nr=projekt_nr, articles=project_articles)
            projects.append(project)
        
        logger.info(f"Created {len(projects)} projects from {len(articles)} articles")
        return projects


# EOF
