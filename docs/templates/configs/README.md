# ⚙️ Configuration Templates

This directory contains Jinja2 templates for generating configuration files. These templates follow the specifications defined in `docs/codex/spec.infrastructure.logging.md` and `docs/codex/spec.project.structure.md`.

## 📁 Available Templates

### config_logging.json.j2
**Purpose:** Logging configuration template for structured logging

**Variables:**
- `{{ log_level }}` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `{{ log_file }}` - Log file path
- `{{ handlers }}` - Logging handlers configuration

**Usage:**
```bash
jinja2 config_logging.json.j2 \
  -D log_level="INFO" \
  -D log_file="logs/app.log" \
  -D handlers='["console", "file"]' \
  > config/logging.json
```

### config_template.json.j2
**Purpose:** General application configuration template

**Variables:**
- `{{ short_code_1 }}` - First configuration code
- `{{ label_1 }}` - First configuration label
- `{{ short_code_2 }}` - Second configuration code
- `{{ label_2 }}` - Second configuration label
- `{{ description }}` - Configuration description

**Usage:**
```bash
jinja2 config_template.json.j2 \
  -D short_code_1="dev" \
  -D label_1="Development" \
  -D short_code_2="prod" \
  -D label_2="Production" \
  -D description="Environment configuration" \
  > config/environment.json
```

## 🚀 How to Use

### 1. **Review the Specifications**
Before using these templates, understand the configuration patterns:
```bash
cat ../../codex/spec.infrastructure.logging.md
cat ../../codex/spec.project.structure.md
```

### 2. **Generate Configuration Files**
Use the templates to create consistent configuration files:
```bash
# Generate logging configuration
jinja2 config_logging.json.j2 -D log_level="DEBUG" > config/logging.json

# Generate application configuration
jinja2 config_template.json.j2 -D description="App settings" > config/app.json
```

### 3. **Load Configuration**
Use the generated configuration files with the helper utilities:
```python
from app.helpers.helper_config_loader import load_config

# Load logging configuration
logging_config = load_config("config/logging.json")

# Load application configuration
app_config = load_config("config/app.json")
```

## 📋 Configuration Patterns

All configuration templates follow these patterns:

1. **Structured Format:** Use JSON for machine-readable configuration
2. **Environment Support:** Support different environments (dev, staging, prod)
3. **Validation:** Include schema validation where appropriate
4. **Documentation:** Include descriptive labels and descriptions
5. **Flexibility:** Allow customization through variables

## 🔗 Related Documentation

- **[Logging Specification](../../codex/spec.infrastructure.logging.md)** - Logging configuration guidelines
- **[Project Structure](../../codex/spec.project.structure.md)** - Overall project organization
- **[Helper Templates](../helpers/)** - Configuration loading utilities

## 🎯 Benefits

Using these configuration templates provides:

- **♻️ Consistency:** Standardized configuration patterns across applications
- **⚡ Speed:** Rapid configuration file generation
- **🔍 Quality:** Pre-validated configurations that follow best practices
- **📚 Maintainability:** Centralized configuration patterns
- **🔧 Flexibility:** Easy customization for different environments

These templates are designed to work with the configuration loading utilities and follow the established infrastructure patterns in the codex.
