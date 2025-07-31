# Codex Specifications Index

This index provides an overview of all specifications and their corresponding templates in the Hello World Codex.

## 📚 Specifications by Domain

### Backend

#### [Backend.Api.Conventions](spec.backend.api.conventions.md)
- **File:** `spec.backend.api.conventions.md`
- **Templates:** None

### Frontend

#### [Backend.Fastapi.Structure](spec.backend.fastapi.structure.md)
- **File:** `spec.backend.fastapi.structure.md`
- **Templates:** route_template_fastapi.py.j2

#### [Documentation.Diagramming](spec.documentation.diagramming.md)
- **File:** `spec.documentation.diagramming.md`
- **Templates:** None

#### [Documentation](spec.documentation.md)
- **File:** `spec.documentation.md`
- **Templates:** None

#### [Infrastructure.Ci.Pipeline](spec.infrastructure.ci.pipeline.md)
- **File:** `spec.infrastructure.ci.pipeline.md`
- **Templates:** None

#### [Infrastructure.Deployment.Local](spec.infrastructure.deployment.local.md)
- **File:** `spec.infrastructure.deployment.local.md`
- **Templates:** None

#### [Infrastructure.Logging](spec.infrastructure.logging.md)
- **File:** `spec.infrastructure.logging.md`
- **Templates:** configs/config_logging.json.j2, logger/logger_template.py.j2

#### [Infrastructure.Makefile](spec.infrastructure.makefile.md)
- **File:** `spec.infrastructure.makefile.md`
- **Templates:** None

#### [Project.Structure](spec.project.structure.md)
- **File:** `spec.project.structure.md`
- **Templates:** template.config_loader.py, template.gitignore, models/model_base.py.j2, components/input_validated_input.py.j2, logger/README.md, validators/validator_template.py.j2, models/model_pydantic_v2.py.j2, validators/README.md, configs/README.md, template.service_logic.py, components/input_dropdown_select.py.j2, docs/README.md, configs/config_template.json.j2, docs/template.openapi_schema.md.j2, template.api_router.py, template.mkdocs.yml, utils/utility_template.py.j2, models/README.md, utils/README.md, logger/logger_template.py.j2, components/README.md, helpers/helper_config_loader.py.j2, template.error_model.py, template.response_model.py, routers/route_template_fastapi.py.j2, routers/README.md, helpers/README.md, routers/route_template_nicegui.py.j2

#### [Quality.Code](spec.quality.code.md)
- **File:** `spec.quality.code.md`
- **Templates:** None

#### [Quality.Security](spec.quality.security.md)
- **File:** `spec.quality.security.md`
- **Templates:** None

#### [Quality.Testing](spec.quality.testing.md)
- **File:** `spec.quality.testing.md`
- **Templates:** None

#### [Ui.Nicegui](spec.ui.nicegui.md)
- **File:** `spec.ui.nicegui.md`
- **Templates:** components/input_validated_input.py.j2, components/input_dropdown_select.py.j2, routers/route_template_nicegui.py.j2

### Infrastructure

#### [Quality.Vcs](spec.quality.vcs.md)
- **File:** `spec.quality.vcs.md`
- **Templates:** None

## 🧩 Templates Overview

### Components

#### input_dropdown_select.py.j2
- **Purpose:** No purpose description found
- **Spec:** None
- **Placeholders:** helper, name, label, helper_func

#### input_validated_input.py.j2
- **Purpose:** No purpose description found
- **Spec:** None
- **Placeholders:** description, name, label, placeholder, regex

### Configs

#### config_logging.json.j2
- **Purpose:** No purpose description found
- **Spec:** None

#### config_template.json.j2
- **Purpose:** No purpose description found
- **Spec:** None
- **Placeholders:** label_1, description, label_2, short_code_1, short_code_2

### Docs

#### template.openapi_schema.md.j2
- **Purpose:** No purpose description found
- **Spec:** None
- **Placeholders:** info.title, path, info.version, else, name, endfor, param.name, details.type, prop, response.description, code, info.description, param.in, endif, operation.operationId

### Helpers

#### helper_config_loader.py.j2
- **Purpose:** No purpose description found
- **Spec:** None
- **Placeholders:** function, config_file, name, label

### Logger

#### logger_template.py.j2
- **Purpose:** No purpose description found
- **Spec:** None

### Models

#### model_base.py.j2
- **Purpose:** No purpose description found
- **Spec:** None
- **Placeholders:** author, project_path, created

#### model_pydantic_v2.py.j2
- **Purpose:** No purpose description found
- **Spec:** None
- **Placeholders:** description, class_name, name, field_description, label

### Routers

#### route_template_fastapi.py.j2
- **Purpose:** No purpose description found
- **Spec:** None
- **Placeholders:** version, resource

#### route_template_nicegui.py.j2
- **Purpose:** No purpose description found
- **Spec:** None
- **Placeholders:** version, page.function, root_function, created, filename, dep, root_call, view_import.module, endfor, page.route, view_import.function, root_route, example_routes, modified, page.description, page.call, root_description

### Templates

#### template.api_router.py
- **Purpose:** No purpose description found
- **Spec:** [spec.project.structure.md](spec.project.structure.md)
- **Placeholders:** resource, created

#### template.config_loader.py
- **Purpose:** No purpose description found
- **Spec:** [spec.project.structure.md](spec.project.structure.md)

#### template.error_model.py
- **Purpose:** No purpose description found
- **Spec:** [spec.project.structure.md](spec.project.structure.md)

#### template.gitignore
- **Purpose:** No purpose description found
- **Spec:** [spec.project.structure.md](spec.project.structure.md)

#### template.mkdocs.yml
- **Purpose:** No purpose description found
- **Spec:** [spec.project.structure.md](spec.project.structure.md)

#### template.response_model.py
- **Purpose:** No purpose description found
- **Spec:** [spec.project.structure.md](spec.project.structure.md)

#### template.service_logic.py
- **Purpose:** No purpose description found
- **Spec:** [spec.project.structure.md](spec.project.structure.md)

#### template.test_api_success.py
- **Purpose:** No purpose description found
- **Spec:** [spec.project.structure.md](spec.project.structure.md)

### Utils

#### utility_template.py.j2
- **Purpose:** No purpose description found
- **Spec:** None

### Validators

#### validator_template.py.j2
- **Purpose:** No purpose description found
- **Spec:** None

## 🏭 Project Examples

> **Real-world implementations using the codex specifications and templates**

### 📦 **Kommissionierung Project**
**Scanner-optimized warehouse picking system**

- **[📄 Project Overview](../projects/kommissionierung/README.md)** - Complete project documentation
- **[🎨 Frontend Specification](../projects/kommissionierung/frontend-specification.md)** - NiceGUI-based scanner interface
- **[🔧 Backend Specification](../projects/kommissionierung/backend-specification.md)** - FastAPI backend architecture

**Key Features:**
- 🔍 **Scanner-optimized workflow** with auto-focus and keyboard-free operation
- 📱 **Multi-screen interface** (Login → Project → Cart → Picking → Completion)
- 🔄 **Real-time progress tracking** with visual and audio feedback
- 📊 **Backend-driven state** for session persistence and recovery

**Technology Stack:**
- **Frontend:** NiceGUI with scanner integration
- **Backend:** FastAPI with REST API and MQTT events
- **Templates Used:** Components, routers, models, validators

### 🛒 **Supermarkt Project**
**Microservice-based supermarket application**

- **[📄 Project Overview](../projects/supermarkt/README.md)** - Complete project documentation

**Key Features:**
- 🏪 **Microservice architecture** with service discovery
- 📊 **Real-time inventory management**
- 🔄 **Event-driven communication** between services
- 📱 **Responsive web interface** for staff and customers

## 🚀 Getting Started

### 1. **Choose Your Project Type**
- **Warehouse Operations** → Follow Kommissionierung project patterns
- **E-commerce/Retail** → Follow Supermarkt project patterns
- **Custom Application** → Use relevant specifications and templates

### 2. **Review Specifications**
```bash
# For frontend applications
cat spec.ui.nicegui.md

# For backend APIs
cat spec.backend.fastapi.structure.md

# For project structure
cat spec.project.structure.md
```

### 3. **Use Templates**
```bash
# Generate FastAPI routes
jinja2 templates/routers/route_template_fastapi.py.j2 -D version="v1" -D resource="users"

# Generate NiceGUI components
jinja2 templates/components/input_validated_input.py.j2 -D name="email" -D label="Email"
```

### 4. **Follow Quality Standards**
- **Code Quality:** `spec.quality.code.md`
- **Testing:** `spec.quality.testing.md`
- **Security:** `spec.quality.security.md`
- **VCS Hygiene:** `spec.quality.vcs.md`

## 📊 Validation

Run validation to ensure consistency:

```bash
make validate-codex
```

This checks:
- Template specification completeness
- Template-spec reference consistency
- Naming convention compliance
- Documentation structure

## 🔗 Quick Links

### Specifications by Domain
- **[Backend](../codex/spec.backend.fastapi.structure.md)** - FastAPI structure and API conventions
- **[Frontend](../codex/spec.ui.nicegui.md)** - NiceGUI patterns and components
- **[Infrastructure](../codex/spec.infrastructure.logging.md)** - Logging, deployment, CI/CD
- **[Quality](../codex/spec.quality.code.md)** - Testing, security, code quality
- **[Documentation](../codex/spec.documentation.md)** - Documentation standards

### Project Examples
- **[Kommissionierung](../projects/kommissionierung/README.md)** - Warehouse picking system
- **[Supermarkt](../projects/supermarkt/README.md)** - Microservice supermarket

### Template Categories
- **[Components](../templates/components/README.md)** - UI component templates
- **[Routers](../templates/routers/README.md)** - API route templates
- **[Models](../templates/models/README.md)** - Data model templates
- **[Utils](../templates/utils/README.md)** - Utility function templates

---

**The Hello World Codex provides a comprehensive framework for building consistent, high-quality Python applications with reusable specifications and templates.**

