# File: frontend/config.py
# Path: frontend/config.py

"""
Configuration management for the frontend application.
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Frontend application settings."""

    # MARK: ━━━ Application Settings ━━━

    app_name: str = Field(
        "Logistics Management System", description="Application name"
    )
    app_version: str = Field("1.0.0", description="Application version")
    debug: bool = Field(True, description="Debug mode")

    # MARK: ━━━ Server Settings ━━━

    host: str = Field("127.0.0.1", description="Frontend host")
    port: int = Field(3000, description="Frontend port")

    # MARK: ━━━ API Settings ━━━

    api_base_url: str = Field(
        "http://localhost:8000", description="Backend API URL"
    )
    api_timeout: int = Field(30, description="API request timeout")

    # MARK: ━━━ UI Settings ━━━

    theme: str = Field("light", description="UI theme")
    language: str = Field("en", description="UI language")

    # MARK: ━━━ Logging Settings ━━━

    log_level: str = Field("INFO", description="Logging level")
    log_format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format",
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
            "default": {
                "format": settings.log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
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
                "filename": "logs/frontend.log",
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
            "nicegui": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }


# MARK: ━━━ Utility Functions ━━━


def validate_config() -> bool:
    """Validate configuration settings."""
    try:
        # Validate API URL format
        if not settings.api_base_url.startswith(("http://", "https://")):
            print(f"Warning: Invalid API URL format: {settings.api_base_url}")
            return False

        # Validate port ranges
        if not (1 <= settings.port <= 65535):
            print(f"Warning: Invalid port number: {settings.port}")
            return False

        return True

    except Exception as e:
        print(f"Configuration validation error: {e}")
        return False


# EOF
