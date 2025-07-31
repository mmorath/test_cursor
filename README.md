# 🏭 Hello World Codex

Welcome to the Hello World Codex project. This is a structured codex and specification framework designed to provide reusable templates and standards for Python-based projects.

## 📚 Documentation Structure

This project is organized into three main areas:

### 1. **Codex Templates** (`docs/codex/`)
Reusable template specifications that can be applied to any project:
- **Backend:** FastAPI structure, API conventions
- **Frontend:** NiceGUI patterns and components
- **Infrastructure:** Logging, deployment, CI/CD
- **Quality:** Testing, security, code quality standards
- **Documentation:** Standards and practices

### 2. **Project Documentation** (`docs/projects/`)
Project-specific documentation and implementations:
- **[Supermarkt Project](docs/projects/supermarkt/README.md)** - Microservice-based supermarket application
- **[Kommissionierung Project](docs/projects/kommissionierung/README.md)** - Scanner-optimized picking system

### 3. **Code Templates** (`docs/templates/`)
Jinja2 templates for generating code based on specifications:
- Python modules and classes
- Configuration files
- Documentation templates
- Component templates

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   make install
   ```

2. **Validate codex structure:**
   ```bash
   make validate-codex
   ```

3. **Start development server:**
   ```bash
   make docs
   ```

4. **Build Docker image:**
   ```bash
   make build
   ```

## 📁 Project Structure

```
helloWorldCodex/
├── docs/
│   ├── codex/                    # Reusable template specifications
│   │   ├── spec.backend.*.md     # Backend standards
│   │   ├── spec.frontend.*.md    # Frontend standards
│   │   ├── spec.infrastructure.*.md # Infrastructure standards
│   │   ├── spec.quality.*.md     # Quality standards
│   │   ├── spec.documentation.*.md # Documentation standards
│   │   ├── spec.project.structure.md # Project structure template
│   │   ├── README.md             # Codex index
│   │   └── validation_report.json # Validation results
│   ├── projects/                 # Project-specific documentation
│   │   ├── supermarkt/           # Supermarkt project docs
│   │   └── kommissionierung/     # Kommissionierung project docs
│   ├── templates/                # Code generation templates
│   │   ├── components/           # UI component templates
│   │   ├── configs/              # Configuration templates
│   │   ├── models/               # Data model templates
│   │   ├── routers/              # Route templates
│   │   └── ...                   # Other template categories
│   └── data/                     # Reference datasets
├── scripts/                      # Utility scripts
│   ├── validate_codex_structure.py # Structure validation
│   ├── simple_refactor_codex.py  # Refactoring tools
│   └── generate_codex_plan.py    # Plan generation
├── requirements.in               # Python dependencies (source)
├── requirements.txt              # Compiled Python dependencies
├── .env.example                  # Environment template
├── .env                          # Environment configuration
├── Dockerfile                    # Container configuration
├── Makefile                      # Development commands
└── README.md                     # This file
```

## 🛠️ Development

### Codex Management
- **Linting:** `make lint`
- **Testing:** `make test`
- **Documentation:** `make docs`
- **Build:** `make build`
- **Validate Codex:** `make validate-codex`
- **Refactor Codex:** `make refactor-codex`

### Environment Setup
- **Setup:** `make setup` - Complete development environment
- **Install:** `make install` - Install dependencies
- **Validate:** `make validate` - Validate environment
- **Clean:** `make clean` - Clean up generated files

## 🎯 How to Use This Codex

### For New Projects

1. **Review Template Specifications:**
   ```bash
   # Browse the codex specifications
   cat docs/codex/README.md
   
   # Focus on relevant domains
   cat docs/codex/spec.backend.fastapi.structure.md
   cat docs/codex/spec.frontend.nicegui.md
   ```

2. **Use Code Templates:**
   ```bash
   # Templates are available in docs/templates/
   ls docs/templates/
   
   # Generate code using Jinja2 templates
   # Example: Generate a FastAPI router
   cat docs/templates/routers/route_template_fastapi.py.j2
   ```

3. **Follow Quality Standards:**
   ```bash
   # Review quality specifications
   cat docs/codex/spec.quality.code.md
   cat docs/codex/spec.quality.testing.md
   ```

4. **Create Project Documentation:**
   ```bash
   # Create project directory
   mkdir docs/projects/your-project/
   
   # Follow the structure of existing projects
   cp -r docs/projects/supermarkt/* docs/projects/your-project/
   ```

### For Template Development

1. **Add New Specifications:**
   ```bash
   # Create new spec file
   touch docs/codex/spec.your-domain.topic.md
   
   # Follow naming convention: spec.<domain>.<topic>.md
   ```

2. **Create Code Templates:**
   ```bash
   # Add templates to appropriate directory
   touch docs/templates/your-category/template_name.py.j2
   
   # Include proper Jinja2 placeholders
   ```

3. **Update References:**
   ```bash
   # Update spec files to reference templates
   # Update templates to reference specs
   # Run validation
   make validate-codex
   ```

## 📊 Validation and Quality

### Codex Validation
The codex includes comprehensive validation to ensure consistency:

```bash
# Run full validation
make validate-codex

# This checks:
# - Template specification completeness
# - Template-spec reference consistency  
# - Naming convention compliance
# - Documentation structure
```

### Quality Standards
All projects should follow the quality specifications:
- **Code Quality:** `docs/codex/spec.quality.code.md`
- **Testing:** `docs/codex/spec.quality.testing.md`
- **Security:** `docs/codex/spec.quality.security.md`
- **VCS Hygiene:** `docs/codex/spec.quality.vcs.md`

## 🔗 Related Documentation

### Codex Specifications
- **[Codex Index](docs/codex/README.md)** - Complete overview of all specifications
- **[Validation Report](docs/codex/validation_report.json)** - Detailed validation results
- **[Optimization Report](docs/codex/OPTIMIZATION_REPORT.md)** - Refactoring documentation

### Project Examples
- **[Supermarkt Project](docs/projects/supermarkt/README.md)** - Microservice application example
- **[Kommissionierung Project](docs/projects/kommissionierung/README.md)** - Scanner-optimized system example

### Template Categories
- **[Components](docs/templates/components/README.md)** - UI component templates
- **[Configs](docs/templates/configs/README.md)** - Configuration templates
- **[Models](docs/templates/models/README.md)** - Data model templates
- **[Routers](docs/templates/routers/README.md)** - Route templates
- **[Utils](docs/templates/utils/README.md)** - Utility templates
- **[Validators](docs/templates/validators/README.md)** - Validation templates
- **[Helpers](docs/templates/helpers/README.md)** - Helper templates
- **[Logger](docs/templates/logger/README.md)** - Logging templates
- **[Docs](docs/templates/docs/README.md)** - Documentation templates

## 🚀 Getting Started with Your Project

1. **Fork or clone this repository**
2. **Review the codex specifications** relevant to your project
3. **Use the templates** to generate your initial code structure
4. **Create project documentation** in `docs/projects/your-project/`
5. **Follow the quality standards** for development
6. **Run validation** regularly to ensure consistency

## 📝 Contributing

When contributing to the codex:

1. **Follow the naming conventions** for specs and templates
2. **Keep specifications project-agnostic** and reusable
3. **Update references** between specs and templates
4. **Run validation** before submitting changes
5. **Document your changes** in the appropriate README files

## 🎯 Benefits

This codex structure provides:

- **♻️ Reusability:** Template specifications can be applied to any project
- **📚 Consistency:** Standardized patterns and practices
- **🛠️ Maintainability:** Clear separation and organization
- **📈 Scalability:** Easy to extend with new specifications and templates
- **🔍 Quality:** Built-in validation and quality standards
- **📖 Documentation:** Comprehensive guides and examples

The Hello World Codex is your foundation for building consistent, high-quality Python applications with reusable patterns and standards.
