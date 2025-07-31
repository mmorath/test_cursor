# File: frontend/app/logger/__init__.py
# Path: frontend/app/logger/__init__.py

"""
Centralized logging initialization for the frontend application.
"""

import logging
import logging.config
from typing import Dict, Any

# Import settings directly to avoid relative import issues
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import settings


def get_logging_config() -> Dict[str, Any]:
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
            "nicegui": {"level": "INFO", "handlers": ["console"], "propagate": False},
        },
    }


def initialize_logging() -> None:
    """Initialize logging configuration."""
    logging_config = get_logging_config()
    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    """Get logger instance for the given name."""
    return logging.getLogger(name)


# EOF
