#!/usr/bin/env python3
"""
Codex Plan Generator for Hello World Codex.
Reads project specifications and generates implementation plans.
"""

import json
from pathlib import Path
from typing import Any, Dict


def generate_codex_plan() -> Dict[str, Any]:
    """Generate a comprehensive codex implementation plan."""
    plan = {
        "project": "Hello World Codex",
        "version": "1.0.0",
        "phases": [
            {
                "phase": "Setup & Infrastructure",
                "tasks": [
                    "Initialize project structure",
                    "Set up development environment",
                    "Configure CI/CD pipeline",
                    "Set up documentation framework",
                ],
                "priority": "high",
            },
            {
                "phase": "Core Development",
                "tasks": [
                    "Implement FastAPI backend",
                    "Create Pydantic models",
                    "Set up database schema",
                    "Implement API endpoints",
                ],
                "priority": "high",
            },
            {
                "phase": "Frontend & UI",
                "tasks": [
                    "Design user interface",
                    "Implement NiceGUI components",
                    "Create responsive layouts",
                    "Add user interactions",
                ],
                "priority": "medium",
            },
            {
                "phase": "Testing & Quality",
                "tasks": [
                    "Write unit tests",
                    "Implement integration tests",
                    "Set up code quality checks",
                    "Performance testing",
                ],
                "priority": "medium",
            },
            {
                "phase": "Documentation & Deployment",
                "tasks": [
                    "Complete API documentation",
                    "Write user guides",
                    "Prepare deployment scripts",
                    "Production deployment",
                ],
                "priority": "low",
            },
        ],
        "estimated_duration": "4-6 weeks",
        "team_size": "2-3 developers",
    }
    return plan


def save_plan(plan: Dict[str, Any], output_path: Path) -> None:
    """Save the generated plan to a JSON file."""
    with open(output_path, "w") as f:
        json.dump(plan, f, indent=2)
    print(f"✅ Codex plan saved to {output_path}")


def print_plan_summary(plan: Dict[str, Any]) -> None:
    """Print a summary of the generated plan."""
    print("🧠 Hello World Codex Implementation Plan")
    print("=" * 50)
    print(f"Project: {plan['project']} v{plan['version']}")
    print(f"Duration: {plan['estimated_duration']}")
    print(f"Team Size: {plan['team_size']}")
    print("\nPhases:")

    for i, phase in enumerate(plan["phases"], 1):
        print(f"\n{i}. {phase['phase']} ({phase['priority']})")
        for task in phase["tasks"]:
            print(f"   • {task}")


def main():
    """Main function to generate and save the codex plan."""
    plan = generate_codex_plan()

    # Print summary
    print_plan_summary(plan)

    # Save to file
    output_path = Path("docs/codex/implementation_plan.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_plan(plan, output_path)


if __name__ == "__main__":
    main()
