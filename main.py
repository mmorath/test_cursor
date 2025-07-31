"""
Main entry point for the Logistics Management System.
"""

import uvicorn
import logging
import logging.config
from pathlib import Path

from config import settings, get_logging_config, validate_configuration
from app.api import app


def setup_logging():
    """Setup logging configuration."""
    logging_config = get_logging_config()
    logging.config.dictConfig(logging_config)

    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")


def main():
    """Main application entry point."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    # Validate configuration
    logger.info("Validating configuration...")
    if not validate_configuration():
        logger.error("Configuration validation failed")
        return 1

    logger.info("Configuration validated successfully")

    # Start the application
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Server will be available at http://{settings.host}:{settings.port}")

    try:
        uvicorn.run(
            "app.api:app",
            host=settings.host,
            port=settings.port,
            reload=settings.debug,
            log_level=settings.log_level.lower()
        )
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())