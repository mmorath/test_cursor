# Infrastructure.Ci.Pipeline

---
title: Infrastructure.Ci.Pipeline
category: specification
status: active
last_updated: 1753967677.0033057
---

# Spezifikation: GitHub Actions Workflow für CI-Pipeline

## Zielsetzung

Diese Spezifikation definiert eine GitHub Actions Pipeline, die bei jedem Push oder Pull-Request automatisch:
- Linter (`black`, `flake8`, `mypy`)
- Tests (`pytest`)
- Dokumentation (`mkdocs build`)
ausführt. Sie dient der Qualitätssicherung und Build-Validierung für alle Projekte mit getrennter Backend- und Frontend-Struktur.

---

## 1. Verzeichnisstruktur

```bash
.github/
└── workflows/
    └── ci.yml


⸻

2. Trigger

Der Workflow wird ausgelöst bei:
	•	Push auf main oder codex/** Branches
	•	Pull Requests auf main oder codex/**

on:
  push:
    branches: ["main", "codex/**"]
  pull_request:
    branches: ["main", "codex/**"]


⸻

3. Anforderungen

Der Workflow soll:
	•	Python 3.11 verwenden
	•	Optional frontend/ prüfen (nur auf Vorhandensein prüfen)
	•	Alle requirements.txt installieren

⸻

4. Pipeline-Schritte

4.1 Setup
	•	Check out Code
	•	Setup Python
	•	Install Abhängigkeiten

4.2 Linting

black --check .
flake8 .
mypy backend/app

4.3 Testing

pytest tests

4.4 Dokumentation

mkdocs build --strict


⸻

5. Beispiel-Workflow (ci.yml)

# File: .github/workflows/ci.yml
# Path: .github/workflows/ci.yml

name: CI Pipeline

on:
  push:
    branches: ["main", "codex/**"]
  pull_request:
    branches: ["main", "codex/**"]

jobs:
  build:
    runs-on: ubuntu-latest
    defaults:
      run:
        shell: bash

    steps:
      - name: ⬇️ Checkout Code
        uses: actions/checkout@v4

      - name: 🐍 Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: 📦 Install Dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          if [ -f backend/requirements.txt ]; then pip install -r backend/requirements.txt; fi
          if [ -f frontend/requirements.txt ]; then pip install -r frontend/requirements.txt; fi

      - name: 🧹 Code Style: Black
        run: black --check .

      - name: 🔍 Linting: Flake8
        run: flake8 .

      - name: 🧠 Type Checking: mypy
        run: mypy backend/app

      - name: 🧪 Tests: pytest
        run: pytest tests

      - name: 📘 Build Documentation
        run: mkdocs build --strict


⸻

6. Erweiterbarkeit
	•	Cache für pip-Abhängigkeiten aktivierbar
	•	Mehrere Python-Versionen testbar (Matrix)
	•	Separate Jobs für Backend/Frontend möglich

⸻

7. Ablage

Bitte speichere wie folgt:

docs/
└── codex/
    └── spec.github_workflow.ci_pipeline.md

.github/
└── workflows/
    └── ci.yml