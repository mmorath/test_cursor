# Quality.Testing

---
title: Quality.Testing
category: specification
status: active
last_updated: 1753967677.0033057
---

# File: spec.tests.md  
# Path: docs/codex/spec.tests.md

# Spezifikation: Teststrategie

## 🎯 Zielsetzung

Diese Spezifikation definiert Konventionen, Struktur und Best Practices für Tests innerhalb des Projekts `supermarkt`. Ziel ist eine hohe Testabdeckung, klare Nachvollziehbarkeit und automatisierte Ausführung im CI/CD-Workflow.

---

## 📦 Teststruktur im Projekt

Alle Tests befinden sich im zentralen Ordner:

```

supermarkt/
├── order\_service/
│   ├── backend/
│   │   └── tests/
│   └── frontend/
│       └── tests/

````

---

## 🧪 Testarten und Anwendungsbereiche

| Testtyp             | Beschreibung                                                                 |
|---------------------|------------------------------------------------------------------------------|
| **Unit Tests**      | Testen einzelne Funktionen oder Klassen isoliert                             |
| **Integrationstests** | Testen das Zusammenspiel mehrerer Komponenten (z. B. API + Datenbank)       |
| **UI-Tests** (Frontend) | Testen Komponenten mit `Playwright`, `pytest + NiceGUI` oder Screenshot-Vergleichen |
| **Smoke Tests**     | Minimale Tests, ob die Applikation überhaupt lauffähig ist                   |

---

## 🧰 Tools & Frameworks

| Zweck             | Tool                         |
|-------------------|------------------------------|
| Python-Tests      | `pytest`, `pytest-cov`       |
| HTTP-Test-Client  | `httpx`, `fastapi.testclient`|
| Coverage-Berichte | `coverage`, `pytest-cov`     |
| UI-Testautomation | (optional) `playwright`, `nicegui.testing` |
| Lint/Static Tests | `flake8`, `mypy`             |

---

## 🛠️ Test Setup & Ausführung

### 📜 Vorbereitung

```bash
# Backend
cd backend
source .venv/bin/activate
pytest --cov=app --cov-report=term-missing

# Frontend
cd frontend
source .venv/bin/activate
pytest --tb=short
````

### 🧪 Testkonventionen

* Jede Testdatei beginnt mit `test_`
* Testfunktionen: `test_<funktion/feature>()`
* Gemeinsame Fixtures in `conftest.py` ablegen

---

## ✅ Namens- und Ordnungsregeln

| Regeltyp              | Konvention            |
| --------------------- | --------------------- |
| Testmodule            | `test_*.py`           |
| Tests für Modelle     | `test_model_*.py`     |
| Tests für Services    | `test_service_*.py`   |
| Tests für Komponenten | `test_component_*.py` |

---

## 🔐 Testen von geschützten APIs

Für geschützte Endpunkte (z. B. mit Auth-Header):

```python
def test_protected_route(client):
    response = client.get("/secure-endpoint", headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200
```

---

## 📊 Coverage-Ziel

* **Ziel:** mindestens `85 %` Code Coverage
* Reports in HTML via:

```bash
pytest --cov=app --cov-report=html
```

Bericht unter `htmlcov/index.html`

---

## 🧪 Beispiel: Pytest für FastAPI

```python
# File: tests/test_api_status.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

---

## 🔄 CI-Integration

Tests werden automatisiert durch GitHub Actions oder GitLab CI/CD ausgeführt:

```yaml
# .github/workflows/ci-test.yml

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest --cov=app
```

---

## 🧼 Erweiterungsmöglichkeiten

* Snapshot-Testing für Komponenten
* UI-Visual Testing mit Playwright
* Backend-Mocking mit `responses` oder `httpx_mock`
* Tests für Event-Handling (MQTT, Websockets)

---

## 📘 Referenzen

* [pytest docs](https://docs.pytest.org/)
* [pytest-cov](https://pypi.org/project/pytest-cov/)
* [NiceGUI Testing](https://nicegui.io/documentation/testing)

```