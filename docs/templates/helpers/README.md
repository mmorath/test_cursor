# 🛠️ Helper Function Templates

This directory contains Jinja2 templates for generating helper functions and utility modules. These templates follow the specifications defined in `docs/codex/spec.project.structure.md`.

## 📁 Available Templates

### helper_config_loader.py.j2
**Purpose:** Configuration loading utility template with error handling

**Variables:**
- `{{ config_file }}` - Configuration file path
- `{{ name }}` - Configuration name
- `{{ function }}` - Function name
- `{{ label }}` - Configuration label

**Usage:**
```bash
jinja2 helper_config_loader.py.j2 \
  -D config_file="config/app.json" \
  -D name="app_config" \
  -D function="load_app_config" \
  -D label="Application Configuration" \
  > app/helpers/config_loader.py
```

## 🚀 How to Use

### 1. **Review the Specification**
Before using these templates, understand the helper patterns:
```bash
cat ../../codex/spec.project.structure.md
```

### 2. **Generate Helpers**
Use the templates to create consistent helper functions:
```bash
# Generate configuration loader
jinja2 helper_config_loader.py.j2 -D config_file="config/logging.json" -D name="logging_config" > app/helpers/logging_loader.py
```

### 3. **Customize Helpers**
Extend the generated helpers with your specific logic:
```python
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def load_app_config(config_path: str = "config/app.json") -> Optional[Dict[str, Any]]:
    """Load application configuration from JSON file."""
    try:
        config_file = Path(config_path)
        if not config_file.exists():
            logger.error(f"Configuration file not found: {config_path}")
            return None

        with open(config_file, 'r') as f:
            config = json.load(f)

        logger.info(f"Loaded configuration from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return None
```

## 📋 Helper Patterns

All helper templates follow these patterns:

1. **Error Handling:** Include comprehensive error handling
2. **Logging:** Add proper logging for debugging and monitoring
3. **Type Hints:** Use proper type annotations
4. **Documentation:** Include clear docstrings with examples
5. **Flexibility:** Support customization through parameters

## 🔗 Related Documentation

- **[Project Structure](../../codex/spec.project.structure.md)** - Overall project organization
- **[Quality Standards](../../codex/spec.quality.code.md)** - Code quality guidelines
- **[Testing Standards](../../codex/spec.quality.testing.md)** - Testing guidelines

## 🎯 Benefits

Using these helper templates provides:

- **♻️ Consistency:** Standardized helper patterns across applications
- **⚡ Speed:** Rapid helper function generation
- **🔍 Quality:** Pre-validated functions that follow best practices
- **📚 Maintainability:** Centralized helper patterns
- **🔧 Reusability:** Modular helper functions that can be shared

These templates are designed to work with the overall project structure and follow the established quality patterns in the codex.
