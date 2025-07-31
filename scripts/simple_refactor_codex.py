#!/usr/bin/env python3
"""
Simple Codex Refactorer

This script performs basic refactoring tasks on the codex structure.
"""

import json
import re
import shutil
from pathlib import Path
from typing import Any

from validate_codex_structure import CodexValidator


class SimpleCodexRefactorer:
    """Simplified refactorer for codex structure optimization."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.docs_path = project_root / "docs"
        self.codex_path = self.docs_path / "codex"
        self.templates_path = self.docs_path / "templates"

        self.spec_renames = {
            "spec.frontend.nicegui.md": "spec.ui.nicegui.md",
            "spec.kommissionierung.overview.md": "spec.project.kommissionierung.overview.md",
            "spec.kommissionierung.frontend.md": "spec.frontend.kommissionierung.md",
            "spec.kommissionierung.backend.md": "spec.backend.kommissionierung.md",
            "spec.project.supermarkt.md": "spec.project.supermarkt.md",
        }

        self.template_references = {
            "spec.backend.fastapi.structure.md": [
                "routers/route_template_fastapi.py.j2"
            ],
            "spec.ui.nicegui.md": [
                "components/input_validated_input.py.j2",
                "components/input_dropdown_select.py.j2",
                "routers/route_template_nicegui.py.j2",
            ],
            "spec.infrastructure.logging.md": [
                "configs/config_logging.json.j2",
                "logger/logger_template.py.j2",
            ],
            "spec.project.structure.md": [
                "template.config_loader.py",
                "template.gitignore",
                "models/model_base.py.j2",
                "components/input_validated_input.py.j2",
                "logger/README.md",
                "validators/validator_template.py.j2",
                "models/model_pydantic_v2.py.j2",
                "validators/README.md",
                "configs/README.md",
                "template.service_logic.py",
                "components/input_dropdown_select.py.j2",
                "docs/README.md",
                "configs/config_template.json.j2",
                "docs/template.openapi_schema.md.j2",
                "template.api_router.py",
                "template.mkdocs.yml",
                "utils/utility_template.py.j2",
                "models/README.md",
                "utils/README.md",
                "logger/logger_template.py.j2",
                "components/README.md",
                "helpers/helper_config_loader.py.j2",
                "template.error_model.py",
                "template.response_model.py",
                "routers/route_template_fastapi.py.j2",
                "routers/README.md",
                "helpers/README.md",
                "routers/route_template_nicegui.py.j2",
            ],
        }

    def rename_specs(self):
        """Rename spec files according to naming conventions."""
        print("🔄 Renaming spec files...")

        for old_name, new_name in self.spec_renames.items():
            old_path = self.codex_path / old_name
            new_path = self.codex_path / new_name

            if old_path.exists() and not new_path.exists():
                shutil.move(str(old_path), str(new_path))
                print(f"  ✅ Renamed {old_name} → {new_name}")

    def fix_template_references(self):
        """Fix template references in spec files."""
        print("🔧 Fixing template references...")

        for spec_file, templates in self.template_references.items():
            spec_path = self.codex_path / spec_file
            if not spec_path.exists():
                continue

            content = spec_path.read_text(encoding="utf-8")

            # Add template references if missing
            if "## Templates" not in content:
                template_section = "\n## Templates\n\n"
                for template in templates:
                    template_section += f"- `{template}`\n"
                content += template_section
                spec_path.write_text(content, encoding="utf-8")
                print(f"  ✅ Added template references to {spec_file}")

    def create_missing_templates(self):
        """Create basic template files if missing."""
        print("📝 Creating missing templates...")

        # Create basic template structure
        basic_templates = {
            "components/input_validated_input.py.j2": '''# Validated Input Component Template
# Generated from: {{ spec_file }}

def create_validated_input(name: str, label: str, validation_rules: str = None):
    """Create a validated input component."""
    return {
        "name": "{{ name }}",
        "label": "{{ label }}",
        "validation_rules": "{{ validation_rules }}",
        "placeholder": "{{ placeholder }}",
        "description": "{{ description }}"
    }
''',
            "components/input_dropdown_select.py.j2": '''# Dropdown Select Component Template
# Generated from: {{ spec_file }}

def create_dropdown_select(name: str, label: str, options: list):
    """Create a dropdown select component."""
    return {
        "name": "{{ name }}",
        "label": "{{ label }}",
        "helper": "{{ helper }}",
        "helper_func": "{{ helper_func }}",
        "options": options
    }
''',
            "routers/route_template_fastapi.py.j2": '''# FastAPI Route Template
# Generated from: {{ spec_file }}

from fastapi import APIRouter, HTTPException
from typing import List, Optional

router = APIRouter(prefix="/{{ version }}/{{ resource }}", tags=["{{ resource }}"])

@router.get("/")
async def get_{{ resource }}(limit: int = 10, offset: int = 0):
    """Get list of {{ resource }}."""
    return {"{{ resource }}": [], "total": 0}

@router.get("/{id}")
async def get_{{ resource[:-1] }}(id: str):
    """Get a specific {{ resource[:-1] }}."""
    return {"id": id, "name": "Example"}
''',
            "routers/route_template_nicegui.py.j2": '''# NiceGUI Route Template
# Generated from: {{ spec_file }}

from nicegui import ui

def create_{{ page.function }}():
    """Create {{ page.description }}."""
    with ui.page("{{ page.route }}"):
        ui.label("{{ page.description }}")
        # Add your components here
        ui.button("{{ page.call }}", on_click=lambda: None)

# Version: {{ version }}
# Created: {{ created }}
# Modified: {{ modified }}
''',
            "models/model_pydantic_v2.py.j2": '''# Pydantic v2 Model Template
# Generated from: {{ spec_file }}

from pydantic import BaseModel, Field
from typing import Optional

class {{ class_name }}(BaseModel):
    """{{ description }}."""

    name: str = Field(..., description="{{ field_description }}")
    label: str = Field(..., description="Display label")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "{{ name }}",
                "label": "{{ label }}"
            }
        }
''',
            "logger/logger_template.py.j2": '''# Logger Template
# Generated from: {{ spec_file }}

import logging
import json
from pathlib import Path

def init_logging(config_path: str = "{{ config_path }}"):
    """Initialize logging with configuration."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        logging.basicConfig(
            level=getattr(logging, config.get('level', 'INFO')),
            format='{{ log_format }}',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(config.get('file', 'app.log'))
            ]
        )

        return True
    except Exception as e:
        print(f"Error initializing logging: {e}")
        return False
''',
            "validators/validator_template.py.j2": '''# Validator Template
# Generated from: {{ spec_file }}

import re
from typing import Tuple, Optional

def {{ validation_name }}(value: str) -> Tuple[bool, Optional[str]]:
    """{{ rules }}."""
    try:
        # Add your validation logic here
        if not value:
            return False, "Value is required"

        # Example validation
        if not re.match(r'^[a-zA-Z0-9]+$', value):
            return False, "Invalid format"

        return True, None
    except Exception as e:
        return False, f"Validation error: {e}"
''',
            "utils/utility_template.py.j2": '''# Utility Template
# Generated from: {{ spec_file }}

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

def {{ function_name }}(*args, **kwargs) -> Optional[Any]:
    """{{ purpose }}."""
    try:
        # Add your utility logic here
        result = None

        logger.info(f"{{ function_name }} completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error in {{ function_name }}: {e}")
        return None
''',
            "helpers/helper_config_loader.py.j2": '''# Config Loader Helper Template
# Generated from: {{ spec_file }}

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def {{ function }}(config_file: str = "{{ config_file }}") -> Optional[Dict[str, Any]]:
    """Load {{ name }} configuration."""
    try:
        config_path = Path(config_file)
        if not config_path.exists():
            logger.error(f"Configuration file not found: {config_file}")
            return None

        with open(config_path, 'r') as f:
            config = json.load(f)

        logger.info(f"Loaded {{ label }} from {config_file}")
        return config
    except Exception as e:
        logger.error(f"Error loading {{ name }}: {e}")
        return None
''',
            "configs/config_logging.json.j2": """{
  "level": "{{ log_level }}",
  "file": "{{ log_file }}",
  "format": "{{ log_format }}",
  "handlers": ["console", "file"]
}""",
            "configs/config_template.json.j2": """{
  "{{ short_code_1 }}": {
    "label": "{{ label_1 }}",
    "description": "{{ description }}"
  },
  "{{ short_code_2 }}": {
    "label": "{{ label_2 }}",
    "description": "{{ description }}"
  }
}""",
            "docs/template.openapi_schema.md.j2": """# OpenAPI Schema Documentation
# Generated from: {{ spec_file }}

## {{ info.title }} v{{ info.version }}

{{ info.description }}

### Endpoints

{% for path, operations in paths.items() %}
#### {{ path }}

{% for method, operation in operations.items() %}
**{{ method.upper() }}** {{ path }}

{{ operation.description }}

**Parameters:**
{% for param in operation.parameters %}
- `{{ param.name }}` ({{ param.in }}) - {{ param.type }}
{% endfor %}

**Responses:**
{% for code, response in operation.responses.items() %}
- `{{ code }}` - {{ response.description }}
{% endfor %}

{% endfor %}
{% endfor %}
""",
        }

        for template_path, content in basic_templates.items():
            full_path = self.templates_path / template_path
            if not full_path.exists():
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")
                print(f"  ✅ Created {template_path}")

    def run(self):
        """Run all refactoring tasks."""
        print("🚀 Starting codex refactoring...")

        self.rename_specs()
        self.fix_template_references()
        self.create_missing_templates()

        print("✅ Refactoring completed!")


def main():
    """Main function."""
    project_root = Path.cwd()
    refactorer = SimpleCodexRefactorer(project_root)
    refactorer.run()


if __name__ == "__main__":
    main()
