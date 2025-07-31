"""
Configuration management for logistics management system.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application settings
    app_name: str = "Logistics Management System"
    app_version: str = "1.0.0"
    debug: bool = False

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000

    # Data settings
    data_directory: str = "docs/data"
    csv_filename: str = "orig.csv"
    json_filename: str = "project.json"

    # Database settings (for future use)
    database_url: Optional[str] = None

    # Logging settings
    log_level: str = "INFO"
    log_file: Optional[str] = None

    # CORS settings
    cors_origins: list = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]

    # Security settings
    secret_key: str = "your-secret-key-here"
    access_token_expire_minutes: int = 30

    # Performance settings
    max_orders_per_page: int = 100
    cache_ttl_seconds: int = 300

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_data_path() -> Path:
    """Get the data directory path."""
    return Path(settings.data_directory)


def get_csv_path() -> Path:
    """Get the CSV file path."""
    return get_data_path() / settings.csv_filename


def get_json_path() -> Path:
    """Get the JSON file path."""
    return get_data_path() / settings.json_filename


def validate_configuration() -> bool:
    """Validate the configuration."""
    try:
        # Check data directory
        data_path = get_data_path()
        if not data_path.exists():
            print(f"Warning: Data directory does not exist: {data_path}")
            return False

        # Check CSV file
        csv_path = get_csv_path()
        if not csv_path.exists():
            print(f"Warning: CSV file does not exist: {csv_path}")
            return False

        # Check JSON file
        json_path = get_json_path()
        if not json_path.exists():
            print(f"Warning: JSON file does not exist: {json_path}")
            return False

        return True

    except Exception as e:
        print(f"Configuration validation error: {e}")
        return False


def create_sample_env_file() -> None:
    """Create a sample .env file."""
    env_content = """# Logistics Management System Configuration

# Application settings
APP_NAME=Logistics Management System
APP_VERSION=1.0.0
DEBUG=false

# Server settings
HOST=0.0.0.0
PORT=8000

# Data settings
DATA_DIRECTORY=docs/data
CSV_FILENAME=orig.csv
JSON_FILENAME=project.json

# Logging settings
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Security settings
SECRET_KEY=your-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Performance settings
MAX_ORDERS_PER_PAGE=100
CACHE_TTL_SECONDS=300
"""

    env_path = Path(".env")
    if not env_path.exists():
        with open(env_path, "w") as f:
            f.write(env_content)
        print("Created sample .env file")
    else:
        print(".env file already exists")


def get_logging_config() -> dict:
    """Get logging configuration."""
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.log_level,
                "formatter": "default",
                "stream": "ext://sys.stdout"
            }
        },
        "root": {
            "level": settings.log_level,
            "handlers": ["console"]
        },
        "loggers": {
            "app": {
                "level": settings.log_level,
                "handlers": ["console"],
                "propagate": False
            }
        }
    }

    # Add file handler if log_file is specified
    if settings.log_file:
        log_path = Path(settings.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        config["handlers"]["file"] = {
            "class": "logging.FileHandler",
            "level": settings.log_level,
            "formatter": "detailed",
            "filename": settings.log_file
        }

        config["root"]["handlers"].append("file")
        config["loggers"]["app"]["handlers"].append("file")

    return config