# 🛣️ Route Templates

This directory contains Jinja2 templates for generating API routes and page definitions. These templates follow the specifications defined in `docs/codex/spec.backend.fastapi.structure.md` and `docs/codex/spec.ui.nicegui.md`.

## 📁 Available Templates

### route_template_fastapi.py.j2
**Purpose:** FastAPI route template with versioning support

**Variables:**
- `{{ version }}` - API version (e.g., v1, v2)
- `{{ resource }}` - Resource name (e.g., users, projects)

**Usage:**
```bash
jinja2 route_template_fastapi.py.j2 \
  -D version="v1" \
  -D resource="users" \
  > app/routes/users.py
```

### route_template_nicegui.py.j2
**Purpose:** NiceGUI page route template with component integration

**Variables:**
- `{{ version }}` - Application version
- `{{ page.route }}` - Page route path
- `{{ page.function }}` - Page function name
- `{{ page.description }}` - Page description
- `{{ page.call }}` - Page function call
- `{{ root_function }}` - Root function name
- `{{ root_route }}` - Root route path
- `{{ root_description }}` - Root description
- `{{ root_call }}` - Root function call
- `{{ filename }}` - File name
- `{{ created }}` - Creation timestamp
- `{{ modified }}` - Modification timestamp
- `{{ dep }}` - Dependencies
- `{{ example_routes }}` - Example route definitions
- `{{ view_import.module }}` - View module import
- `{{ view_import.function }}` - View function import

**Usage:**
```bash
jinja2 route_template_nicegui.py.j2 \
  -D version="1.0.0" \
  -D page.route="/login" \
  -D page.function="login_page" \
  -D page.description="User login page" \
  > app/routes/login.py
```

## 🚀 How to Use

### 1. **Review the Specifications**
Before using these templates, understand the routing patterns:
```bash
cat ../../codex/spec.backend.fastapi.structure.md
cat ../../codex/spec.ui.nicegui.md
```

### 2. **Generate Routes**
Use the templates to create consistent route definitions:
```bash
# Generate FastAPI route
jinja2 route_template_fastapi.py.j2 -D version="v1" -D resource="projects" > app/routes/projects.py

# Generate NiceGUI page
jinja2 route_template_nicegui.py.j2 -D page.route="/dashboard" -D page.function="dashboard_page" > app/routes/dashboard.py
```

### 3. **Customize Routes**
Extend the generated routes with your specific endpoints and logic:
```python
from fastapi import APIRouter, HTTPException
from app.models.project import ProjectModel

router = APIRouter(prefix="/v1/projects", tags=["projects"])

@router.get("/{project_id}")
async def get_project(project_id: str):
    # Your implementation here
    pass
```

## 📋 Route Patterns

All route templates follow these patterns:

1. **Versioning:** Support API versioning for backward compatibility
2. **Resource-Based:** Organize routes by resource/entity
3. **Documentation:** Include proper docstrings and descriptions
4. **Error Handling:** Include appropriate error handling
5. **Validation:** Use Pydantic models for request/response validation

## 🔗 Related Documentation

- **[FastAPI Structure](../../codex/spec.backend.fastapi.structure.md)** - Backend routing guidelines
- **[NiceGUI Specification](../../codex/spec.ui.nicegui.md)** - Frontend routing patterns
- **[API Conventions](../../codex/spec.backend.api.conventions.md)** - API design patterns
- **[Quality Standards](../../codex/spec.quality.code.md)** - Code quality guidelines

## 🎯 Benefits

Using these route templates provides:

- **♻️ Consistency:** Standardized routing patterns across applications
- **⚡ Speed:** Rapid route generation with proper structure
- **🔍 Quality:** Pre-validated routes that follow best practices
- **📚 Maintainability:** Centralized routing patterns
- **🔧 Versioning:** Built-in support for API versioning

These templates are designed to work with FastAPI and NiceGUI, following the established backend and frontend patterns in the codex.
