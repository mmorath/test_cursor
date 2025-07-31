#!/usr/bin/env python3
"""
Codex Structure Refactoring Script

This script systematically refactors the docs/codex and docs/templates structure
to fix validation issues, standardize naming conventions, and ensure proper
references between specs and templates.
"""

import json
import re
import shutil
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class RefactoringAction:
    """Represents a refactoring action to be performed."""
    action_type: str  # 'rename', 'update_reference', 'create_template', 'fix_content'
    description: str
    source_path: Path = None
    target_path: Path = None
    content_updates: Dict[str, str] = None


class CodexRefactorer:
    """Main refactorer class for codex structure optimization."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.docs_path = project_root / "docs"
        self.codex_path = self.docs_path / "codex"
        self.templates_path = self.docs_path / "templates"
        
        self.actions: List[RefactoringAction] = []
        
        # Standardized naming mappings
        self.spec_renames = {
            'spec.frontend.nicegui.md': 'spec.ui.nicegui.md',
            'spec.kommissionierung.overview.md': 'spec.project.kommissionierung.overview.md',
            'spec.kommissionierung.backend.md': 'spec.backend.kommissionierung.md',
            'spec.kommissionierung.frontend.md': 'spec.frontend.kommissionierung.md',
            'spec.structure.fastapi.md': 'spec.backend.fastapi.structure.md',
            'spec.structure.cleaned.md': 'spec.project.structure.md',
            'spec.project.supermarkt.md': 'spec.project.supermarkt.md',  # Already correct
            'spec.makefile.native.md': 'spec.infrastructure.makefile.md',
            'spec.deployment.local.md': 'spec.infrastructure.deployment.local.md',
            'spec.docs.diagramming.md': 'spec.documentation.diagramming.md',
            'spec.github_workflow.ci_pipeline.md': 'spec.infrastructure.ci.pipeline.md',
            'spec.api_conventions.md': 'spec.backend.api.conventions.md',
            'spec.code_quality.md': 'spec.quality.code.md',
            'spec.test.md': 'spec.quality.testing.md',
            'spec.security.md': 'spec.quality.security.md',
            'spec.docs.md': 'spec.documentation.md',
            'spec.logging.md': 'spec.infrastructure.logging.md',
            'spec.vcs_hygiene.md': 'spec.quality.vcs.md'
        }
        
        # Template reference mappings
        self.template_references = {
            'spec.ui.nicegui.md': [
                'components/input_validated_input.py.j2',
                'components/input_dropdown_select.py.j2',
                'routers/route_template_nicegui.py.j2'
            ],
            'spec.infrastructure.logging.md': [
                'logger/logger_template.py.j2',
                'configs/config_logging.json.j2'
            ],
            'spec.project.structure.md': [
                'models/model_base.py.j2',
                'models/model_pydantic_v2.py.j2',
                'routers/route_template_fastapi.py.j2',
                'components/input_dropdown_select.py.j2',
                'utils/utility_template.py.j2',
                'validators/validator_template.py.j2',
                'helpers/helper_config_loader.py.j2',
                'docs/template.openapi_schema.md.j2',
                'configs/config_template.json.j2'
            ],
            'spec.backend.fastapi.structure.md': [
                'routers/route_template_fastapi.py.j2',
                'models/model_base.py.j2',
                'models/model_pydantic_v2.py.j2'
            ],
            'spec.documentation.md': [
                'docs/template.openapi_schema.md.j2',
                'template.mkdocs.yml'
            ],
            'spec.infrastructure.makefile.md': [
                'template.gitignore'
            ],
            'spec.quality.testing.md': [
                'template.test_api_success.py'
            ]
        }
    
    def plan_refactoring(self) -> None:
        """Plan all refactoring actions."""
        print("📋 Planning refactoring actions...")
        
        # Plan spec renames
        self._plan_spec_renames()
        
        # Plan template reference updates
        self._plan_template_reference_updates()
        
        # Plan content improvements
        self._plan_content_improvements()
        
        # Plan missing template creation
        self._plan_missing_templates()
    
    def _plan_spec_renames(self) -> None:
        """Plan renaming of spec files to follow naming conventions."""
        for old_name, new_name in self.spec_renames.items():
            old_path = self.codex_path / old_name
            new_path = self.codex_path / new_name
            
            if old_path.exists() and old_path != new_path:
                self.actions.append(RefactoringAction(
                    action_type='rename',
                    description=f"Rename spec from {old_name} to {new_name}",
                    source_path=old_path,
                    target_path=new_path
                ))
    
    def _plan_template_reference_updates(self) -> None:
        """Plan updates to template references in spec files."""
        for spec_name, template_refs in self.template_references.items():
            spec_path = self.codex_path / spec_name
            
            if spec_path.exists():
                content = spec_path.read_text(encoding='utf-8')
                updated_content = self._update_template_references(content, template_refs)
                
                if content != updated_content:
                    self.actions.append(RefactoringAction(
                        action_type='update_reference',
                        description=f"Update template references in {spec_name}",
                        source_path=spec_path,
                        content_updates={'content': updated_content}
                    ))
    
    def _update_template_references(self, content: str, template_refs: List[str]) -> str:
        """Update template references in spec content."""
        # Remove old template references
        content = re.sub(r'`[^`]*\.j2`', '', content)
        content = re.sub(r'`[^`]*_template\.py`', '', content)
        
        # Add new template references section
        if template_refs:
            refs_section = "\n## 📋 Related Templates\n\n"
            for ref in template_refs:
                refs_section += f"- `{ref}`\n"
            refs_section += "\n"
            
            # Add before the last section
            sections = content.split('\n## ')
            if len(sections) > 1:
                sections.insert(-1, refs_section)
                content = '\n## '.join(sections)
            else:
                content += refs_section
        
        return content
    
    def _plan_content_improvements(self) -> None:
        """Plan improvements to spec content."""
        for spec_path in self.codex_path.glob("spec.*.md"):
            content = spec_path.read_text(encoding='utf-8')
            improved_content = self._improve_spec_content(content, spec_path.name)
            
            if content != improved_content:
                self.actions.append(RefactoringAction(
                    action_type='fix_content',
                    description=f"Improve content in {spec_path.name}",
                    source_path=spec_path,
                    content_updates={'content': improved_content}
                ))
    
    def _improve_spec_content(self, content: str, spec_name: str) -> str:
        """Improve spec content with better structure and metadata."""
        # Add frontmatter if missing
        if not content.startswith('---'):
            frontmatter = f"""---
title: {spec_name.replace('spec.', '').replace('.md', '').replace('_', ' ').title()}
category: specification
status: active
last_updated: {Path().stat().st_mtime}
---

"""
            content = frontmatter + content
        
        # Ensure proper heading structure
        if not content.startswith('# '):
            title = spec_name.replace('spec.', '').replace('.md', '').replace('_', ' ').title()
            content = f"# {title}\n\n{content}"
        
        return content
    
    def _plan_missing_templates(self) -> None:
        """Plan creation of missing template files."""
        missing_templates = [
            'docs/template.openapi_schema.md.j2',
            'utils/utility_template.py.j2',
            'validators/validator_template.py.j2',
            'helpers/helper_config_loader.py.j2'
        ]
        
        for template_path in missing_templates:
            full_path = self.templates_path / template_path
            if not full_path.exists():
                self.actions.append(RefactoringAction(
                    action_type='create_template',
                    description=f"Create missing template {template_path}",
                    target_path=full_path,
                    content_updates={'template_content': self._generate_template_content(template_path)}
                ))
    
    def _generate_template_content(self, template_path: str) -> str:
        """Generate content for missing templates."""
        if template_path.endswith('.py.j2'):
            return self._generate_python_template(template_path)
        elif template_path.endswith('.md.j2'):
            return self._generate_markdown_template(template_path)
        else:
            return self._generate_generic_template(template_path)
    
    def _generate_python_template(self, template_path: str) -> str:
        """Generate Python template content."""
        template_name = Path(template_path).stem
        class_name = ''.join(word.capitalize() for word in template_name.split('_'))
        
        return f"""# File: {{{{ app_name }}}}/{{{{ template_path.replace('.j2', '') }}}}
# AUTO-GENERATED BY CODEX

# Template for {{{{ class_name }}}}
# Purpose: {{{{ template_purpose }}}}

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class {{{{ class_name }}}}:
    \"\"\"{{{{ template_purpose }}}}\"\"\"
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {{{{}}}}
        logger.info("Initialized {{{{ class_name }}}}")
    
    def process(self, data: Any) -> Any:
        \"\"\"Process data according to template specification.\"\"\"
        logger.debug("Processing data with {{{{ class_name }}}}")
        # TODO: Implement processing logic
        return data
"""
    
    def _generate_markdown_template(self, template_path: str) -> str:
        """Generate Markdown template content."""
        template_name = Path(template_path).stem
        
        return f"""# {{{{ title }}}}

{{{{ description }}}}

## Overview

This template is generated from {{ template_path }}.

## Usage

```python
# Example usage
{{{{ usage_example }}}}
```

## Configuration

{{{{ configuration_details }}}}

## Examples

{{{{ examples }}}
"""
    
    def _generate_generic_template(self, template_path: str) -> str:
        """Generate generic template content."""
        return f"""# Template: {{ template_path }}

This template is generated from {{ template_path }}.

## Purpose

{{{{ template_purpose }}}}

## Usage

{{{{ usage_instructions }}}}

## Configuration

{{{{ configuration_options }}}}
"""
    
    def execute_refactoring(self) -> None:
        """Execute all planned refactoring actions."""
        print(f"🚀 Executing {len(self.actions)} refactoring actions...")
        
        for i, action in enumerate(self.actions, 1):
            print(f"[{i}/{len(self.actions)}] {action.description}")
            
            try:
                if action.action_type == 'rename':
                    self._execute_rename(action)
                elif action.action_type == 'update_reference':
                    self._execute_update_reference(action)
                elif action.action_type == 'fix_content':
                    self._execute_fix_content(action)
                elif action.action_type == 'create_template':
                    self._execute_create_template(action)
                
                print(f"   ✅ Completed")
                
            except Exception as e:
                print(f"   ❌ Failed: {e}")
    
    def _execute_rename(self, action: RefactoringAction) -> None:
        """Execute a rename action."""
        if action.source_path and action.target_path:
            action.target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(action.source_path), str(action.target_path))
    
    def _execute_update_reference(self, action: RefactoringAction) -> None:
        """Execute a reference update action."""
        if action.source_path and action.content_updates:
            action.source_path.write_text(
                action.content_updates['content'], 
                encoding='utf-8'
            )
    
    def _execute_fix_content(self, action: RefactoringAction) -> None:
        """Execute a content fix action."""
        if action.source_path and action.content_updates:
            action.source_path.write_text(
                action.content_updates['content'], 
                encoding='utf-8'
            )
    
    def _execute_create_template(self, action: RefactoringAction) -> None:
        """Execute a template creation action."""
        if action.target_path and action.content_updates:
            action.target_path.parent.mkdir(parents=True, exist_ok=True)
            action.target_path.write_text(
                action.content_updates['template_content'], 
                encoding='utf-8'
            )
    
    def print_plan(self) -> None:
        """Print the refactoring plan."""
        print("\n" + "="*60)
        print("📋 REFACTORING PLAN")
        print("="*60)
        
        for i, action in enumerate(self.actions, 1):
            print(f"{i}. [{action.action_type.upper()}] {action.description}")
            if action.source_path:
                print(f"   Source: {action.source_path}")
            if action.target_path:
                print(f"   Target: {action.target_path}")
            print()


def main():
    """Main function to run the refactoring."""
    project_root = Path(__file__).parent.parent
    refactorer = CodexRefactorer(project_root)
    
    try:
        # Plan refactoring
        refactorer.plan_refactoring()
        
        # Show plan
        refactorer.print_plan()
        
        # Ask for confirmation
        response = input("\nProceed with refactoring? (y/N): ")
        if response.lower() != 'y':
            print("Refactoring cancelled.")
            return
        
        # Execute refactoring
        refactorer.execute_refactoring()
        
        print("\n✅ Refactoring completed successfully!")
        print("Run 'python scripts/validate_codex_structure.py' to verify changes.")
        
    except Exception as e:
        print(f"❌ Refactoring failed: {e}")
        return 1


if __name__ == "__main__":
    main() 