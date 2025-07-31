# 🎨 UI Component Templates

This directory contains Jinja2 templates for generating reusable UI components, primarily for NiceGUI-based frontend applications. These templates follow the specifications defined in `docs/codex/spec.ui.nicegui.md`.

## 📁 Available Templates

### input_dropdown_select.py.j2
**Purpose:** Dropdown selection component with helper functions

**Variables:**
- `{{ name }}` - Component name/identifier
- `{{ label }}` - Display label
- `{{ helper }}` - Helper text
- `{{ helper_func }}` - Helper function name

**Usage:**
```bash
jinja2 input_dropdown_select.py.j2 \
  -D name="project_select" \
  -D label="Select Project" \
  -D helper="Choose a project from the list" \
  -D helper_func="get_projects" \
  > app/components/project_select.py
```

### input_validated_input.py.j2
**Purpose:** Validated input field component with regex validation

**Variables:**
- `{{ name }}` - Field name
- `{{ label }}` - Display label
- `{{ placeholder }}` - Input placeholder text
- `{{ regex }}` - Validation regex pattern
- `{{ description }}` - Field description

**Usage:**
```bash
jinja2 input_validated_input.py.j2 \
  -D name="project_number" \
  -D label="Project Number" \
  -D placeholder="Enter 6-digit project number" \
  -D regex="^[0-9]{6}$" \
  -D description="Must be exactly 6 digits" \
  > app/components/project_input.py
```

## 🚀 How to Use

### 1. **Review the Specification**
Before using these templates, understand the NiceGUI component patterns:
```bash
cat ../../codex/spec.ui.nicegui.md
```

### 2. **Generate Components**
Use the templates to create consistent UI components:
```bash
# Generate a dropdown component
jinja2 input_dropdown_select.py.j2 -D name="status" -D label="Status" > app/components/status_select.py

# Generate a validated input
jinja2 input_validated_input.py.j2 -D name="email" -D label="Email" > app/components/email_input.py
```

### 3. **Customize as Needed**
Modify the generated components to fit your specific requirements while maintaining consistency.

## 📋 Component Patterns

All components follow these patterns:

1. **Consistent Naming:** Use descriptive, consistent naming conventions
2. **Validation:** Include appropriate validation rules
3. **Helper Functions:** Provide helper functions for data loading
4. **Error Handling:** Include proper error handling and user feedback
5. **Logging:** Add appropriate logging for debugging

## 🔗 Related Documentation

- **[NiceGUI Specification](../../codex/spec.ui.nicegui.md)** - Frontend development guidelines
- **[Project Structure](../../codex/spec.project.structure.md)** - Overall project organization
- **[Quality Standards](../../codex/spec.quality.code.md)** - Code quality guidelines

## 🎯 Benefits

Using these component templates provides:

- **♻️ Consistency:** Standardized UI patterns across applications
- **⚡ Speed:** Rapid component generation
- **🔍 Quality:** Pre-validated components that follow best practices
- **📚 Maintainability:** Centralized component patterns
- **🎨 UX:** Consistent user experience across applications

These templates are designed to work with NiceGUI and follow the established frontend patterns in the codex.
