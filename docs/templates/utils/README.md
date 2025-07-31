# 🔧 Utility Function Templates

This directory contains Jinja2 templates for generating utility functions and helper modules. These templates follow the specifications defined in `docs/codex/spec.project.structure.md`.

## 📁 Available Templates

### utility_template.py.j2
**Purpose:** General utility function template with logging and error handling

**Variables:**
- `{{ function_name }}` - Function name
- `{{ purpose }}` - Function purpose/description

**Usage:**
```bash
jinja2 utility_template.py.j2 \
  -D function_name="format_date" \
  -D purpose="Format date strings" \
  > app/utils/date_utils.py
```

## 🚀 How to Use

### 1. **Review the Specification**
Before using these templates, understand the utility patterns:
```bash
cat ../../codex/spec.project.structure.md
```

### 2. **Generate Utilities**
Use the templates to create consistent utility functions:
```bash
# Generate utility function
jinja2 utility_template.py.j2 -D function_name="validate_email" -D purpose="Email validation" > app/utils/validation.py
```

### 3. **Customize Utilities**
Extend the generated utilities with your specific logic:
```python
import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def validate_email(email: str) -> Optional[str]:
    """Validate email format and return cleaned email or None."""
    try:
        # Your validation logic here
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return email.lower().strip()
        return None
    except Exception as e:
        logger.error(f"Error validating email: {e}")
        return None
```

## 📋 Utility Patterns

All utility templates follow these patterns:

1. **Logging:** Include proper logging for debugging and monitoring
2. **Error Handling:** Include try-catch blocks for robust error handling
3. **Type Hints:** Use proper type annotations for better code clarity
4. **Documentation:** Include descriptive docstrings
5. **Testing:** Support unit testing with clear input/output expectations

## 🔗 Related Documentation

- **[Project Structure](../../codex/spec.project.structure.md)** - Overall project organization
- **[Quality Standards](../../codex/spec.quality.code.md)** - Code quality guidelines
- **[Testing Standards](../../codex/spec.quality.testing.md)** - Testing guidelines

## 🎯 Benefits

Using these utility templates provides:

- **♻️ Consistency:** Standardized utility patterns across applications
- **⚡ Speed:** Rapid utility function generation
- **🔍 Quality:** Pre-validated utilities that follow best practices
- **📚 Maintainability:** Centralized utility patterns
- **🔧 Reusability:** Modular utility functions that can be shared

These templates are designed to work with the overall project structure and follow the established quality patterns in the codex.
