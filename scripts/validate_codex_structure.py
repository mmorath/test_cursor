#!/usr/bin/env python3
"""
Codex Structure Validation and Optimization Script

This script validates the entire docs/codex and docs/templates structure,
ensuring consistency, completeness, and proper references between specs and 
templates.
"""

import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class ValidationIssue:
    """Represents a validation issue found during analysis."""

    severity: str  # 'error', 'warning', 'info'
    category: str  # 'spec', 'template', 'reference', 'naming'
    message: str
    file_path: str
    line_number: int = 0
    suggestion: str = ""


@dataclass
class SpecInfo:
    """Information about a specification file."""

    name: str
    path: Path
    title: str = ""
    domain: str = ""
    references: List[str] = None
    template_references: List[str] = None

    def __post_init__(self):
        if self.references is None:
            self.references = []
        if self.template_references is None:
            self.template_references = []


@dataclass
class TemplateInfo:
    """Information about a template file."""

    name: str
    path: Path
    purpose: str = ""
    spec_reference: str = ""
    syntax_valid: bool = True
    placeholders: List[str] = None

    def __post_init__(self):
        if self.placeholders is None:
            self.placeholders = []


class CodexValidator:
    """Main validator class for codex structure analysis."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.docs_path = project_root / "docs"
        self.codex_path = self.docs_path / "codex"
        self.templates_path = self.docs_path / "templates"

        self.specs: Dict[str, SpecInfo] = {}
        self.templates: Dict[str, TemplateInfo] = {}
        self.issues: List[ValidationIssue] = []

        # Domain mappings for categorization
        self.domain_patterns = {
            "frontend": ["frontend", "ui", "nicegui", "components"],
            "backend": ["backend", "api", "fastapi", "service"],
            "infrastructure": ["deployment", "docker", "ci", "github", "makefile"],
            "documentation": ["docs", "mkdocs", "diagramming"],
            "quality": ["test", "lint", "code_quality", "security"],
            "logging": ["logging", "logger"],
            "configuration": ["config", "configs"],
            "models": ["models", "pydantic"],
            "routing": ["routers", "routes"],
        }

    def analyze_structure(self) -> None:
        """Analyze the entire codex structure."""
        print("🔍 Analyzing codex structure...")

        # Collect all specs
        self._collect_specs()

        # Collect all templates
        self._collect_templates()

        # Analyze references
        self._analyze_references()

        # Validate naming conventions
        self._validate_naming_conventions()

        # Check for orphaned files
        self._check_orphaned_files()

        # Validate template syntax
        self._validate_template_syntax()

    def _collect_specs(self) -> None:
        """Collect all specification files from codex directory.

        Note: Project-specific documentation has been moved to docs/projects/
        to separate reusable template specifications from project-specific docs.
        """
        for spec_file in self.codex_path.glob("spec.*.md"):
            if spec_file.name == "README.md":
                continue

            spec_info = self._parse_spec_file(spec_file)
            self.specs[spec_file.name] = spec_info

    def _parse_spec_file(self, spec_path: Path) -> SpecInfo:
        """Parse a specification file and extract information."""
        content = spec_path.read_text(encoding="utf-8")

        # Extract title
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else spec_path.stem

        # Determine domain
        domain = self._determine_domain(spec_path.name, content)

        # Extract template references
        template_refs = self._extract_template_references(content)

        return SpecInfo(
            name=spec_path.name,
            path=spec_path,
            title=title,
            domain=domain,
            template_references=template_refs,
        )

    def _determine_domain(self, filename: str, content: str) -> str:
        """Determine the domain of a specification based on filename and content."""
        text_to_check = f"{filename} {content.lower()}"

        for domain, patterns in self.domain_patterns.items():
            if any(pattern in text_to_check for pattern in patterns):
                return domain

        return "general"

    def _extract_template_references(self, content: str) -> List[str]:
        """Extract template file references from spec content."""
        references = []

        # Look for template references in various formats
        patterns = [
            r"`([^`]+\.j2)`",
            r"`([^`]+\.py\.j2)`",
            r"`([^`]+_template\.py)`",
            r"templates/([^`\s]+)",
            r"codex/templates/([^`\s]+)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content)
            references.extend(matches)

        return list(set(references))

    def _collect_templates(self) -> None:
        """Collect all template files."""
        for template_file in self.templates_path.rglob("*.j2"):
            template_info = self._parse_template_file(template_file)
            self.templates[template_file.name] = template_info

        # Also collect non-j2 template files
        for template_file in self.templates_path.rglob("template.*"):
            if template_file.suffix != ".j2":
                template_info = self._parse_template_file(template_file)
                self.templates[template_file.name] = template_info

    def _parse_template_file(self, template_path: Path) -> TemplateInfo:
        """Parse a template file and extract information."""
        content = template_path.read_text(encoding="utf-8")

        # Extract purpose from comments
        purpose = self._extract_template_purpose(content)

        # Extract placeholders
        placeholders = self._extract_placeholders(content)

        # Find corresponding spec
        spec_ref = self._find_spec_reference(template_path.name, content)

        return TemplateInfo(
            name=template_path.name,
            path=template_path,
            purpose=purpose,
            spec_reference=spec_ref,
            placeholders=placeholders,
        )

    def _extract_template_purpose(self, content: str) -> str:
        """Extract purpose description from template comments."""
        # Look for purpose in comments
        purpose_patterns = [
            r'"""([^"]*purpose[^"]*)"""',
            r"#\s*Purpose:\s*(.+)",
            r"#\s*Template for:\s*(.+)",
        ]

        for pattern in purpose_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return "No purpose description found"

    def _extract_placeholders(self, content: str) -> List[str]:
        """Extract Jinja2 placeholders from template content."""
        placeholders = []

        # Jinja2 variable patterns
        patterns = [
            r"\{\{\s*(\w+)\s*\}\}",
            r"\{\%\s*(\w+)\s*\%\}",
            r"\{\{\s*(\w+\.\w+)\s*\}\}",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content)
            placeholders.extend(matches)

        return list(set(placeholders))

    def _find_spec_reference(self, template_name: str, content: str) -> str:
        """Find which spec file references this template."""
        # Remove .j2 extension for matching
        base_name = template_name.replace(".j2", "")

        for spec_name, spec_info in self.specs.items():
            if base_name in spec_info.template_references:
                return spec_name

        return ""

    def _analyze_references(self) -> None:
        """Analyze references between specs and templates."""
        print("🔗 Analyzing spec-template references...")

        # Check for missing template references
        for spec_name, spec_info in self.specs.items():
            for template_ref in spec_info.template_references:
                if not any(
                    template_ref in template_name
                    for template_name in self.templates.keys()
                ):
                    self.issues.append(
                        ValidationIssue(
                            severity="error",
                            category="reference",
                            message=f"Template reference '{template_ref}' not found",
                            file_path=str(spec_info.path),
                            suggestion=f"Check if template exists or update reference",
                        )
                    )

        # Check for templates without spec references
        for template_name, template_info in self.templates.items():
            if not template_info.spec_reference:
                self.issues.append(
                    ValidationIssue(
                        severity="warning",
                        category="reference",
                        message=f"Template '{template_name}' has no spec reference",
                        file_path=str(template_info.path),
                        suggestion="Add reference in appropriate spec file",
                    )
                )

    def _validate_naming_conventions(self) -> None:
        """Validate naming conventions across specs and templates."""
        print("📝 Validating naming conventions...")

        # Check spec naming consistency
        spec_pattern = re.compile(r"spec\.([^.]+)\.md")
        for spec_name in self.specs.keys():
            if not spec_pattern.match(spec_name):
                self.issues.append(
                    ValidationIssue(
                        severity="warning",
                        category="naming",
                        message=f"Spec file '{spec_name}' doesn't follow naming convention",
                        file_path=str(self.specs[spec_name].path),
                        suggestion="Rename to follow 'spec.<domain>.<topic>.md' pattern",
                    )
                )

        # Check template naming consistency
        for template_name in self.templates.keys():
            if not (
                template_name.endswith(".j2") or template_name.startswith("template.")
            ):
                self.issues.append(
                    ValidationIssue(
                        severity="warning",
                        category="naming",
                        message=f"Template '{template_name}' doesn't follow naming convention",
                        file_path=str(self.templates[template_name].path),
                        suggestion="Use .j2 extension or 'template.' prefix",
                    )
                )

    def _check_orphaned_files(self) -> None:
        """Check for orphaned files without proper references."""
        print("🔍 Checking for orphaned files...")

        # Check for specs without template references
        for spec_name, spec_info in self.specs.items():
            if not spec_info.template_references:
                self.issues.append(
                    ValidationIssue(
                        severity="info",
                        category="spec",
                        message=f"Spec '{spec_name}' has no template references",
                        file_path=str(spec_info.path),
                        suggestion="Consider adding template references or mark as documentation-only",
                    )
                )

    def _validate_template_syntax(self) -> None:
        """Validate Jinja2 template syntax."""
        print("🔧 Validating template syntax...")

        for template_name, template_info in self.templates.items():
            if template_name.endswith(".j2"):
                content = template_info.path.read_text(encoding="utf-8")

                # Check for basic Jinja2 syntax issues
                if "{{" in content and "}}" not in content:
                    self.issues.append(
                        ValidationIssue(
                            severity="error",
                            category="template",
                            message=f"Unclosed Jinja2 variable in '{template_name}'",
                            file_path=str(template_info.path),
                            suggestion="Check for missing closing braces",
                        )
                    )

                if "{%" in content and "%}" not in content:
                    self.issues.append(
                        ValidationIssue(
                            severity="error",
                            category="template",
                            message=f"Unclosed Jinja2 block in '{template_name}'",
                            file_path=str(template_info.path),
                            suggestion="Check for missing closing tags",
                        )
                    )

    def generate_index(self) -> str:
        """Generate a comprehensive index of all specs and templates."""
        print("📋 Generating codex index...")

        # Group specs by domain
        domain_specs = defaultdict(list)
        for spec_info in self.specs.values():
            domain_specs[spec_info.domain].append(spec_info)

        # Generate markdown index
        index_content = """# Codex Specifications Index

This index provides an overview of all specifications and their corresponding templates in the Hello World Codex.

## 📚 Specifications by Domain

"""

        for domain, specs in sorted(domain_specs.items()):
            index_content += f"\n### {domain.title()}\n\n"

            for spec in sorted(specs, key=lambda x: x.name):
                index_content += f"#### [{spec.title}]({spec.name})\n"
                index_content += f"- **File:** `{spec.name}`\n"
                if spec.template_references:
                    index_content += (
                        f"- **Templates:** {', '.join(spec.template_references)}\n"
                    )
                else:
                    index_content += "- **Templates:** None\n"
                index_content += "\n"

        # Add template overview
        index_content += "\n## 🧩 Templates Overview\n\n"

        template_by_type = defaultdict(list)
        for template_info in self.templates.values():
            template_type = template_info.path.parent.name
            template_by_type[template_type].append(template_info)

        for template_type, templates in sorted(template_by_type.items()):
            index_content += f"\n### {template_type.title()}\n\n"

            for template in sorted(templates, key=lambda x: x.name):
                index_content += f"#### {template.name}\n"
                index_content += f"- **Purpose:** {template.purpose}\n"
                if template.spec_reference:
                    index_content += f"- **Spec:** [{template.spec_reference}]({template.spec_reference})\n"
                else:
                    index_content += "- **Spec:** None\n"
                if template.placeholders:
                    index_content += (
                        f"- **Placeholders:** {', '.join(template.placeholders)}\n"
                    )
                index_content += "\n"

        return index_content

    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive validation report."""
        report = {
            "summary": {
                "total_specs": len(self.specs),
                "total_templates": len(self.templates),
                "total_issues": len(self.issues),
                "errors": len([i for i in self.issues if i.severity == "error"]),
                "warnings": len([i for i in self.issues if i.severity == "warning"]),
                "info": len([i for i in self.issues if i.severity == "info"]),
            },
            "issues": [
                {
                    "severity": issue.severity,
                    "category": issue.category,
                    "message": issue.message,
                    "file": issue.file_path,
                    "suggestion": issue.suggestion,
                }
                for issue in self.issues
            ],
            "specs": {
                name: {
                    "title": spec.title,
                    "domain": spec.domain,
                    "template_references": spec.template_references,
                }
                for name, spec in self.specs.items()
            },
            "templates": {
                name: {
                    "purpose": template.purpose,
                    "spec_reference": template.spec_reference,
                    "placeholders": template.placeholders,
                }
                for name, template in self.templates.items()
            },
        }

        return report

    def print_summary(self) -> None:
        """Print a summary of the validation results."""
        print("\n" + "=" * 60)
        print("📊 VALIDATION SUMMARY")
        print("=" * 60)

        print(f"📄 Specifications: {len(self.specs)}")
        print(f"🧩 Templates: {len(self.templates)}")
        print(f"❌ Errors: {len([i for i in self.issues if i.severity == 'error'])}")
        print(
            f"⚠️  Warnings: {len([i for i in self.issues if i.severity == 'warning'])}"
        )
        print(f"ℹ️  Info: {len([i for i in self.issues if i.severity == 'info'])}")

        if self.issues:
            print("\n🔍 ISSUES FOUND:")
            for issue in sorted(self.issues, key=lambda x: (x.severity, x.category)):
                severity_icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}[
                    issue.severity
                ]
                print(f"{severity_icon} [{issue.severity.upper()}] {issue.message}")
                print(f"   File: {issue.file_path}")
                if issue.suggestion:
                    print(f"   Suggestion: {issue.suggestion}")
                print()


def main():
    """Main function to run the validation."""
    project_root = Path(__file__).parent.parent
    validator = CodexValidator(project_root)

    try:
        validator.analyze_structure()
        validator.print_summary()

        # Generate index
        index_content = validator.generate_index()
        index_path = validator.codex_path / "README.md"
        index_path.write_text(index_content, encoding="utf-8")
        print(f"✅ Generated index at {index_path}")

        # Generate report
        report = validator.generate_report()
        report_path = validator.codex_path / "validation_report.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"✅ Generated report at {report_path}")

        # Exit with error code if there are critical issues
        if any(issue.severity == "error" for issue in validator.issues):
            print("❌ Validation failed due to errors!")
            sys.exit(1)
        else:
            print("✅ Validation completed successfully!")

    except Exception as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
