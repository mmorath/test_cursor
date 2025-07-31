# ✅ Input Validation Templates

This directory contains Jinja2 templates for generating input validation functions and modules. These templates follow the specifications defined in `docs/codex/spec.project.structure.md`.

## 📁 Available Templates

### validator_template.py.j2
**Purpose:** Input validation function template with comprehensive validation rules

**Variables:**
- `{{ validation_name }}` - Validation function name
- `{{ rules }}` - Validation rules and constraints

**Usage:**
```bash
jinja2 validator_template.py.j2 \
  -D validation_name="validate_project_number" \
  -D rules="6-digit numeric format" \
  > app/validators/project_validators.py
```

## 🚀 How to Use

### 1. **Review the Specification**
Before using these templates, understand the validation patterns:
```bash
cat ../../codex/spec.project.structure.md
```

### 2. **Generate Validators**
Use the templates to create consistent validation functions:
```bash
# Generate validation function
jinja2 validator_template.py.j2 -D validation_name="validate_email" -D rules="email format validation" > app/validators/email_validators.py
```

### 3. **Customize Validators**
Extend the generated validators with your specific validation logic:
```python
import re
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def validate_project_number(project_number: str) -> Tuple[bool, Optional[str]]:
    """Validate project number format (6 digits)."""
    try:
        # Validation logic
        if not project_number:
            return False, "Project number is required"
        
        if not re.match(r'^[0-9]{6}$', project_number):
            return False, "Project number must be exactly 6 digits"
        
        return True, None
    except Exception as e:
        logger.error(f"Error validating project number: {e}")
        return False, "Validation error occurred"
```

## 📋 Validation Patterns

All validation templates follow these patterns:

1. **Return Format:** Return tuple of (is_valid, error_message)
2. **Error Handling:** Include comprehensive error handling
3. **Logging:** Add proper logging for debugging
4. **Type Hints:** Use proper type annotations
5. **Documentation:** Include clear docstrings with examples

## 🔗 Related Documentation

- **[Project Structure](../../codex/spec.project.structure.md)** - Overall project organization
- **[Quality Standards](../../codex/spec.quality.code.md)** - Code quality guidelines
- **[Testing Standards](../../codex/spec.quality.testing.md)** - Testing guidelines

## 🎯 Benefits

Using these validation templates provides:

- **♻️ Consistency:** Standardized validation patterns across applications
- **⚡ Speed:** Rapid validation function generation
- **🔍 Quality:** Pre-validated functions that follow best practices
- **📚 Maintainability:** Centralized validation patterns
- **🔧 Reusability:** Modular validation functions that can be shared

These templates are designed to work with the overall project structure and follow the established quality patterns in the codex.
