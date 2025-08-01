# 🧩 Code Templates

This directory contains Jinja2 templates for generating code based on the specifications defined in `docs/codex/`. These templates provide reusable code patterns that can be applied to any project following the codex standards.

## 📁 Template Categories

### 🎨 Components (`components/`)
UI component templates for frontend applications:
- **input_dropdown_select.py.j2** - Dropdown selection component
- **input_validated_input.py.j2** - Validated input field component

### ⚙️ Configs (`configs/`)
Configuration file templates:
- **config_logging.json.j2** - Logging configuration template
- **config_template.json.j2** - General configuration template

### 📝 Docs (`docs/`)
Documentation templates:
- **template.openapi_schema.md.j2** - OpenAPI schema documentation

### 🛠️ Helpers (`helpers/`)
Helper utility templates:
- **helper_config_loader.py.j2** - Configuration loader utility

### 📊 Logger (`logger/`)
Logging system templates:
- **logger_template.py.j2** - Logger initialization template

### 🏗️ Models (`models/`)
Data model templates:
- **model_base.py.j2** - Base model template
- **model_pydantic_v2.py.j2** - Pydantic v2 model template

### 🛣️ Routers (`routers/`)
Route definition templates:
- **route_template_fastapi.py.j2** - FastAPI route template
- **route_template_nicegui.py.j2** - NiceGUI route template

### 🔧 Utils (`utils/`)
Utility function templates:
- **utility_template.py.j2** - General utility function template

### ✅ Validators (`validators/`)
Input validation templates:
- **validator_template.py.j2** - Input validation template

### 📄 Templates (`templates/`)
General file templates:
- **template.api_router.py** - API router template
- **template.config_loader.py** - Configuration loader template
- **template.error_model.py** - Error model template
- **template.gitignore** - Git ignore template
- **template.mkdocs.yml** - MkDocs configuration template
- **template.response_model.py** - Response model template
- **template.service_logic.py** - Service logic template
- **template.test_api_success.py** - API test template

## 🚀 How to Use Templates

### 1. **Understand the Specification**
Before using a template, review the corresponding specification in `docs/codex/`:
```bash
# Example: For FastAPI routes
cat docs/codex/spec.backend.fastapi.structure.md
```

### 2. **Choose the Right Template**
Select the template that matches your needs:
```bash
# Example: For creating a new FastAPI route
cat docs/templates/routers/route_template_fastapi.py.j2
```

### 3. **Customize the Template**
Modify the template with your specific requirements:
```bash
# Example: Generate a custom route
jinja2 docs/templates/routers/route_template_fastapi.py.j2 \
  -D resource=users \
  -D version=v1 \
  > app/routes/users.py
```

### 4. **Follow the Pattern**
Use the generated code as a starting point and follow the patterns established in the specification.

## 📋 Template Variables

Each template uses Jinja2 variables that you can customize:

### Common Variables
- `{{ app_name }}` - Application name
- `{{ version }}` - API version
- `{{ resource }}` - Resource name
- `{{ class_name }}` - Class name
- `{{ function_name }}` - Function name

### Component-Specific Variables
- `{{ name }}` - Field name
- `{{ label }}` - Display label
- `{{ validation_rules }}` - Validation rules
- `{{ placeholder }}` - Input placeholder

### Configuration Variables
- `{{ log_level }}` - Logging level
- `{{ log_file }}` - Log file path
- `{{ config_path }}` - Configuration file path

## 🔗 Template-Specification Mapping

Each template corresponds to one or more specifications:

| Template | Specification | Purpose |
|----------|---------------|---------|
| `route_template_fastapi.py.j2` | `spec.backend.fastapi.structure.md` | FastAPI route generation |
| `input_validated_input.py.j2` | `spec.ui.nicegui.md` | NiceGUI input component |
| `logger_template.py.j2` | `spec.infrastructure.logging.md` | Logging setup |
| `model_pydantic_v2.py.j2` | `spec.project.structure.md` | Data model generation |

## 🛠️ Template Development

### Creating New Templates

1. **Follow Naming Convention:**
   ```
   template_name.py.j2
   ```

2. **Include Proper Documentation:**
   ```jinja2
   # File: {{ app_name }}/{{ file_path }}
   # AUTO-GENERATED BY CODEX
   # Template: {{ template_name }}
   # Purpose: {{ template_purpose }}
   ```

3. **Use Descriptive Variables:**
   ```jinja2
   class {{ class_name }}:
       """{{ class_description }}"""
   ```

4. **Include Usage Examples:**
   ```jinja2
   # Usage:
   # jinja2 {{ template_name }} -D class_name=MyClass -D description="My description"
   ```

### Template Best Practices

1. **Keep Templates Focused:** Each template should serve a single, clear purpose
2. **Use Descriptive Variables:** Variable names should be self-explanatory
3. **Include Documentation:** Add comments explaining the template's purpose
4. **Follow Code Standards:** Generated code should follow the quality specifications
5. **Test Templates:** Verify that generated code works correctly

## 📊 Validation

Templates are validated against specifications:

```bash
# Run template validation
make validate-codex

# This checks:
# - Template syntax correctness
# - Template-specification references
# - Variable consistency
# - Generated code quality
```

## 🔗 Related Documentation

- **[Codex Specifications](../codex/README.md)** - Template specifications
- **[Project Examples](../projects/)** - Example implementations
- **[Quality Standards](../codex/spec.quality.code.md)** - Code quality guidelines

## 🎯 Benefits

Using these templates provides:

- **♻️ Consistency:** Standardized code patterns across projects
- **⚡ Speed:** Rapid code generation for common patterns
- **🔍 Quality:** Pre-validated code that follows best practices
- **📚 Maintainability:** Centralized templates that can be updated
- **🎯 Focus:** Developers can focus on business logic rather than boilerplate

The templates are designed to work together with the codex specifications to provide a complete development framework for Python applications.
