# File: spec.env.python.md
# Path: docs/codex/spec.env.python.md

# Specification: Python Virtual Environment & Dependency Management

## Purpose

This specification defines the standard practice for Python environment isolation and dependency management across **all frontend and backend microservices** in this project. The approach ensures consistency, cross-platform compatibility, and clean separation of dependencies per service.

---

## MARK: ━━━ Environment Strategy ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Each **microservice** (whether backend or frontend) must be developed and executed in a **dedicated Python virtual environment**.
- This ensures that Python packages and their dependencies are isolated from:
  - Other services
  - The global system environment
  - The OS-level package manager (e.g., `apt`, `dnf`)

---

## MARK: ━━━ Dependency Management ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Dependencies are **not pinned manually** in `requirements.txt`.
- Instead, we use a **`requirements.in` file** as the *source of truth* for all required packages.
- The `.in` file is compiled into a **platform-specific `requirements.txt`** using [pip-tools](https://github.com/jazzband/pip-tools):

  ```bash
  pip-compile requirements.in