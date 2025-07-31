# 🏗️ Data Model Templates

This directory contains Jinja2 templates for generating Pydantic data models. These templates follow the specifications defined in `docs/codex/spec.project.structure.md` and support both base models and Pydantic v2 models.

## 📁 Available Templates

### model_base.py.j2
**Purpose:** Base model template with common functionality

**Variables:**
- `{{ author }}` - Model author
- `{{ project_path }}` - Project path
- `{{ created }}` - Creation timestamp

**Usage:**
```bash
jinja2 model_base.py.j2 \
  -D author="John Doe" \
  -D project_path="app/models" \
  -D created="2024-01-01" \
  > app/models/base.py
```

### model_pydantic_v2.py.j2
**Purpose:** Pydantic v2 model template with validation

**Variables:**
- `{{ class_name }}` - Model class name
- `{{ name }}` - Model name
- `{{ field_description }}` - Field description
- `{{ label }}` - Display label
- `{{ description }}` - Model description

**Usage:**
```bash
jinja2 model_pydantic_v2.py.j2 \
  -D class_name="UserModel" \
  -D name="user" \
  -D field_description="User information" \
  -D label="User" \
  -D description="User data model" \
  > app/models/user.py
```

## 🚀 How to Use

### 1. **Review the Specification**
Before using these templates, understand the model patterns:
```bash
cat ../../codex/spec.project.structure.md
```

### 2. **Generate Models**
Use the templates to create consistent data models:
```bash
# Generate base model
jinja2 model_base.py.j2 -D author="Team" > app/models/base.py

# Generate Pydantic model
jinja2 model_pydantic_v2.py.j2 -D class_name="ProjectModel" > app/models/project.py
```

### 3. **Customize Models**
Extend the generated models with your specific fields and validation:
```python
from app.models.base import BaseModel
from pydantic import Field

class ProjectModel(BaseModel):
    project_id: str = Field(..., description="Project identifier")
    name: str = Field(..., description="Project name")
    status: str = Field(default="active", description="Project status")
```

## 📋 Model Patterns

All model templates follow these patterns:

1. **Pydantic v2:** Use latest Pydantic features and syntax
2. **Type Hints:** Include proper type annotations
3. **Validation:** Include field validation and constraints
4. **Documentation:** Add descriptive docstrings and field descriptions
5. **Inheritance:** Support model inheritance from base classes

## 🔗 Related Documentation

- **[Project Structure](../../codex/spec.project.structure.md)** - Overall project organization
- **[API Conventions](../../codex/spec.backend.api.conventions.md)** - API design patterns
- **[Quality Standards](../../codex/spec.quality.code.md)** - Code quality guidelines

## 🎯 Benefits

Using these model templates provides:

- **♻️ Consistency:** Standardized data model patterns across applications
- **⚡ Speed:** Rapid model generation with proper structure
- **🔍 Quality:** Pre-validated models that follow best practices
- **📚 Maintainability:** Centralized model patterns
- **🔧 Type Safety:** Proper type hints and validation

These templates are designed to work with FastAPI and Pydantic, following the established backend patterns in the codex.
