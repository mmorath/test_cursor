# File: backend/config.py
# Path: backend/config.py

"""
Configuration management for the logistics management system.
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""

    # MARK: ━━━ Application Settings ━━━

    app_name: str = Field("Logistics Management System", description="Application name")
    app_version: str = Field("1.0.0", description="Application version")
    debug: bool = Field(False, description="Debug mode")

    # MARK: ━━━ Server Settings ━━━

    host: str = Field("0.0.0.0", description="Server host")
    port: int = Field(8000, description="Server port")

    # MARK: ━━━ Data Settings ━━━

    data_dir: str = Field("../docs/data", description="Data directory path")
    csv_file: str = Field("orig.csv", description="CSV data file")
    json_file: str = Field("project.json", description="JSON data file")

    # MARK: ━━━ CORS Settings ━━━

    cors_origins: List[str] = Field(
        ["http://localhost:3000", "http://127.0.0.1:3000"],
        description="Allowed CORS origins",
    )
    cors_allow_credentials: bool = Field(True, description="Allow CORS credentials")
    cors_allow_methods: List[str] = Field(
        ["GET", "POST", "PUT", "DELETE", "OPTIONS"], description="Allowed CORS methods"
    )
    cors_allow_headers: List[str] = Field(["*"], description="Allowed CORS headers")

    # MARK: ━━━ Logging Settings ━━━

    log_level: str = Field("INFO", description="Logging level")
    log_format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Log format"
    )

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        case_sensitive = False


# MARK: ━━━ Settings Instance ━━━

settings = Settings()


# MARK: ━━━ Logging Configuration ━━━


def get_logging_config() -> dict:
    """Get logging configuration dictionary."""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": settings.log_format, "datefmt": "%Y-%m-%d %H:%M:%S"},
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.log_level,
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": settings.log_level,
                "formatter": "detailed",
                "filename": "logs/app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "": {
                "level": settings.log_level,
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "uvicorn": {"level": "INFO", "handlers": ["console"], "propagate": False},
            "fastapi": {"level": "INFO", "handlers": ["console"], "propagate": False},
        },
    }


# MARK: ━━━ Utility Functions ━━━


def get_data_path() -> str:
    """Get absolute path to data directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, settings.data_dir)


def validate_config() -> bool:
    """Validate configuration settings."""
    try:
        # Validate data directory exists
        data_path = get_data_path()
        if not os.path.exists(data_path):
            print(f"Warning: Data directory does not exist: {data_path}")
            return False

        # Validate required files exist
        csv_path = os.path.join(data_path, settings.csv_file)
        json_path = os.path.join(data_path, settings.json_file)

        if not os.path.exists(csv_path):
            print(f"Warning: CSV file not found: {csv_path}")
            return False

        if not os.path.exists(json_path):
            print(f"Warning: JSON file not found: {json_path}")
            return False

        return True

    except Exception as e:
        print(f"Configuration validation error: {e}")
        return False


# EOF
