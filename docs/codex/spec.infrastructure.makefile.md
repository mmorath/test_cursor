# Infrastructure.Makefile

---
title: Infrastructure.Makefile
category: specification
status: active
last_updated: 1753967677.0033057
---

# File: spec.makefile.native.md
# Path: docs/codex/spec.makefile.native.md

###############################################################################
# Spezifikation: Native Makefile – Supermarkt Microservices
#
# Beschreibung:
#   Dieses Makefile dient der lokalen (nicht-containerisierten) Verwaltung des
#   Supermarkt-Microservice-Projekts. Es stellt Targets für Installation,
#   Kompilierung, Ausführung, Tests, Linting, Dokumentation und vollständige
#   Projektbereinigung bereit.
#
# Autor: Matthias Morath
# Version: 1.1.0
# License: MIT
###############################################################################

## MARK: ━━━ Anforderungen ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Python ≥ 3.11
- [`pip-tools`](https://github.com/jazzband/pip-tools) installiert
- Unterstützt Back- und Frontend mit jeweils eigenem `.venv`
- MkDocs für Dokumentation (`mkdocs`, `mkdocs-material`)

---

## MARK: ━━━ Targets ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### `make install`

Initialisiert zwei virtuelle Umgebungen und installiert die Abhängigkeiten:

- `backend/.venv` für das Backend
- `frontend/.venv` für das Frontend
- Kompiliert `requirements.txt` aus `requirements.in` mit `pip-compile`

### `make compile`

Kompiliert `requirements.txt` für Backend und Frontend neu:

- Ausführung über vorhandene `.venv`
- Wichtig nach Änderung von `requirements.in`

### `make run`

Startet Backend und Frontend parallel:

- Backend via `python backend/app/main.py`
- Frontend via `python frontend/app/main.py`
- Verwendet native `.venv`-Interpreter

### `make test`

Führt Tests im Backend und Frontend aus:

- Erwartet `pytest` installiert
- Testpfade: `backend/tests/`, `frontend/tests/`

### `make lint`

Lintet Codebasis mit `flake8`:

- Überprüft ausschließlich `app`-Ordner in Backend und Frontend

### `make docs`

Erzeugt statisches HTML-Dokumentations-Output via `mkdocs build`

### `make serve-docs`

Startet lokalen Webserver unter `http://127.0.0.1:8000` via `mkdocs serve`

---

## MARK: ━━━ Erweiterte Bereinigung ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### `make clean`

Löscht ausschließlich die `.venv`-Ordner:

- `backend/.venv`
- `frontend/.venv`

### `make clean-all`

Löscht zusätzlich:

| Element              | Beschreibung                                    |
| -------------------- | ----------------------------------------------- |
| `.venv`              | Virtuelle Umgebungen für Back-/Frontend         |
| `__pycache__`        | Python Cache-Ordner                             |
| `*.pyc`              | Kompilierte Python-Dateien                      |
| `.mypy_cache`        | Cache von `mypy`                                |
| `.pytest_cache`      | Cache von `pytest`                              |
| `htmlcov/`           | Coverage Reports (optional)                     |
| `site/`              | MkDocs Build-Ordner                             |

Empfohlene Implementierung in Makefile:

```make
clean-all:
	find . -type d -name '__pycache__' -exec rm -r {} +;
	find . -type d -name '.mypy_cache' -exec rm -r {} +;
	find . -type d -name '.pytest_cache' -exec rm -r {} +;
	find . -type f -name '*.pyc' -delete;
	rm -rf backend/.venv frontend/.venv htmlcov site