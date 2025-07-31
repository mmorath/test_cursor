# File: template.config_loader.py
# Path: backend/app/helpers/helper_config_<topic>.py

"""
Helper: Configuration Loader
Description:
    Loads and validates JSON configuration with _meta block and jsonschema.

Author: Matthias Morath
"""

# MARK: ━━━ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import json
import logging
from pathlib import Path
from jsonschema import validate
from config.schema_<topic> import SCHEMA_<TOPIC>

# MARK: ━━━ Logger ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logger = logging.getLogger(__name__)

# MARK: ━━━ Loader Function ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def load_<topic>_config(path: str = "config/config_<topic>.json") -> dict:
    """Loads and validates a <topic> configuration file.

    Args:
        path (str): Path to the JSON config file.

    Returns:
        dict: Parsed and validated config dictionary.

    Raises:
        ValueError: If _meta block is missing or validation fails.
    """
    config_path = Path(path)
    data = json.loads(config_path.read_text(encoding="utf-8"))
    
    if "_meta" not in data:
        raise ValueError("Missing _meta in config")

    validate(instance=data, schema=SCHEMA_<TOPIC>)
    
    meta = data["_meta"]
    logger.info(
        "Loaded %s (%s) by %s – %s",
        config_path.name,
        meta.get("version"),
        meta.get("author"),
        meta.get("description")
    )
    
    return data

# EOF
