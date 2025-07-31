# 📊 Logging Templates

This directory contains Jinja2 templates for generating logging configuration and initialization modules. These templates follow the specifications defined in `docs/codex/spec.infrastructure.logging.md`.

## 📁 Available Templates

### logger_template.py.j2
**Purpose:** Logger initialization template with configuration loading

**Variables:**
- `{{ config_path }}` - Configuration file path
- `{{ log_format }}` - Log format string

**Usage:**
```bash
jinja2 logger_template.py.j2 \
  -D config_path="config/logging.json" \
  -D log_format="%(asctime)s | %(levelname)s | %(name)s | %(message)s" \
  > app/logger/logger_config.py
```

## 🚀 How to Use

### 1. **Review the Specification**
Before using these templates, understand the logging patterns:
```bash
cat ../../codex/spec.infrastructure.logging.md
```

### 2. **Generate Logger Configuration**
Use the templates to create consistent logging setup:
```bash
# Generate logger configuration
jinja2 logger_template.py.j2 -D config_path="config/logging.json" > app/logger/logger_config.py
```

### 3. **Initialize Logging**
Use the generated logger configuration in your application:
```python
from app.logger.logger_config import init_logging

# Initialize logging at application startup
init_logging("config/logging.json")

# Use logger in your modules
import logging
logger = logging.getLogger(__name__)

logger.info("Application started")
logger.debug("Debug information")
logger.warning("Warning message")
logger.error("Error occurred")
```

## 📋 Logging Patterns

All logging templates follow these patterns:

1. **Configuration-Based:** Use JSON configuration files for flexibility
2. **Structured Logging:** Include timestamp, level, module, and message
3. **Multiple Handlers:** Support console and file logging
4. **Error Handling:** Include proper error handling for logging setup
5. **Environment Support:** Support different log levels for different environments

## 🔗 Related Documentation

- **[Logging Specification](../../codex/spec.infrastructure.logging.md)** - Logging configuration guidelines
- **[Project Structure](../../codex/spec.project.structure.md)** - Overall project organization
- **[Quality Standards](../../codex/spec.quality.code.md)** - Code quality guidelines

## 🎯 Benefits

Using these logging templates provides:

- **♻️ Consistency:** Standardized logging patterns across applications
- **⚡ Speed:** Rapid logging setup generation
- **🔍 Quality:** Pre-validated logging that follows best practices
- **📚 Maintainability:** Centralized logging patterns
- **🔧 Flexibility:** Easy customization for different environments

These templates are designed to work with the infrastructure specifications and follow the established logging patterns in the codex.
