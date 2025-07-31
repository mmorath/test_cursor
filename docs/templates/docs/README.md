# 📝 Documentation Templates

This directory contains Jinja2 templates for generating documentation files. These templates follow the specifications defined in `docs/codex/spec.documentation.md`.

## 📁 Available Templates

### template.openapi_schema.md.j2
**Purpose:** OpenAPI schema documentation template with comprehensive API documentation

**Variables:**
- `{{ info.title }}` - API title
- `{{ info.version }}` - API version
- `{{ info.description }}` - API description
- `{{ path }}` - API path
- `{{ param.name }}` - Parameter name
- `{{ param.in }}` - Parameter location (path, query, header)
- `{{ details.type }}` - Parameter type
- `{{ response.description }}` - Response description
- `{{ operation.operationId }}` - Operation ID
- `{{ code }}` - HTTP status code
- `{{ prop }}` - Property name

**Usage:**
```bash
jinja2 template.openapi_schema.md.j2 \
  -D info.title="My API" \
  -D info.version="1.0.0" \
  -D info.description="API documentation" \
  > docs/api_schema.md
```

## 🚀 How to Use

### 1. **Review the Specification**
Before using these templates, understand the documentation patterns:
```bash
cat ../../codex/spec.documentation.md
```

### 2. **Generate Documentation**
Use the templates to create consistent documentation:
```bash
# Generate API documentation
jinja2 template.openapi_schema.md.j2 -D info.title="Project API" > docs/api.md
```

### 3. **Customize Documentation**
Extend the generated documentation with your specific content:
```markdown
# My API Documentation

## Overview
This API provides endpoints for managing projects and users.

## Authentication
All endpoints require authentication via API key.

## Endpoints

### GET /api/v1/projects
Retrieve a list of projects.

**Parameters:**
- `limit` (query): Number of projects to return (default: 10)
- `offset` (query): Number of projects to skip (default: 0)

**Response:**
```json
{
  "projects": [
    {
      "id": "string",
      "name": "string",
      "status": "string"
    }
  ],
  "total": "integer"
}
```
```

## 📋 Documentation Patterns

All documentation templates follow these patterns:

1. **Structured Format:** Use consistent markdown formatting
2. **Comprehensive Coverage:** Include all necessary sections
3. **Examples:** Provide practical examples and code snippets
4. **Cross-References:** Include links to related documentation
5. **Maintainability:** Easy to update and maintain

## 🔗 Related Documentation

- **[Documentation Standards](../../codex/spec.documentation.md)** - Documentation guidelines
- **[Project Structure](../../codex/spec.project.structure.md)** - Overall project organization
- **[API Conventions](../../codex/spec.backend.api.conventions.md)** - API documentation patterns

## 🎯 Benefits

Using these documentation templates provides:

- **♻️ Consistency:** Standardized documentation patterns across applications
- **⚡ Speed:** Rapid documentation generation
- **🔍 Quality:** Pre-validated documentation that follows best practices
- **📚 Maintainability:** Centralized documentation patterns
- **🔧 Clarity:** Clear and comprehensive documentation

These templates are designed to work with the documentation specifications and follow the established documentation patterns in the codex.
