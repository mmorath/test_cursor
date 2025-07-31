### 📄 File: `docs/codex/spec.code_headers.md`
### 📁 Location: `docs/codex/`

---

# 🧾 Specification: Python Code Headers & Footers

## 🎯 Purpose

This specification defines the **minimum required header and footer** for all Python source files in this project. It ensures **traceability**, **documentation clarity**, and **code consistency** across all generated or manually written code in this repository.

---

## ✅ Requirements

Every Python file **must include**:

### 1. **Header Block** at the **top of the file** (starting on line 1):

```python
# File: <relative/path/to/file.py>
# Description: <Short description of what this file/module does>
# Author: Matthias Morath
# Created: YYYY-MM-DD
```

#### ✅ Example:

```python
# File: app/api/v1/health.py
# Description: Health check endpoint for monitoring service availability.
# Author: Matthias Morath
# Created: 2025-07-23
```

---

### 2. **Optional Extension** in the header:

If the file contains reusable logic, complex behavior, or exposed functions/classes, it is recommended to add:

```python
# Usage:
#   This module can be imported using:
#       from app.api.v1.health import health_check
#   It provides a FastAPI route that can be probed by Kubernetes or monitoring tools.
#
# Dependencies:
#   - fastapi
#   - logging
```

This is optional but **highly encouraged** for reusable or critical modules.

---

### 3. **Footer Block** at the **end of the file**:

```python
#EOF
```

---

## 🧑‍💻 Coding Style Guidance

* All header comments must **start at line 1**, with no preceding whitespace.
* Maintain 79-character line length where possible.
* Use `#` for all header comment lines to ensure valid syntax and linter compliance.
* The `#EOF` footer should be on a line by itself with no trailing code or comments.

---

## 📌 Enforcement and Automation

These headers and footers **must** be added by:

* Code generation tools like Codex.
* Manual developers and contributors via pre-commit hooks (TBD).
* Verified during code linting (e.g., using `flake8` plugins or custom pre-commit checks).

---

## 📁 File Types Affected

Applies to all files with the `.py` extension in the following folders:

* `app/`
* `tests/`
* `scripts/`
* `utils/`

---

## 🧪 Verification Checklist

| Requirement                   | Enforced? | How            |
| ----------------------------- | --------- | -------------- |
| Header with metadata          | ✅         | Codex template |
| Optional usage + dependencies | ⛔️        | Optional       |
| `#EOF` at end of file         | ✅         | Codex template |

---
