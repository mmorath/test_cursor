# Quality.Code

---
title: Quality.Code
category: specification
status: active
last_updated: 1753967677.0033057
---

# Code Quality Guidelines

This specification defines how all code should be written, structured, and validated across services. It is enforced for both backend and frontend components (e.g. FastAPI, Nicegui, CLI tools).

---

## 1. General Conventions

* Max line length: **79 characters**

* File names: `snake_case.py`

* Function names: `snake_case`

* Class names: `PascalCase`

* Constants: `UPPER_CASE`

* All files must start with a **file header**, e.g.:

  ```python
  # File: model_article.py
  # Path: backend/app/models/model_article.py
  ```

* All files must end with a **footer marker**:

  ```python
  # EOF
  ```

* Use `MARK:` comments to structure sections clearly:

  ```python
  # MARK: ━━━ Datenbankmodelle ━━━
  ```

---

## 2. Folder and Naming Conventions

### Folder names

| Purpose         | Folder name   |
| --------------- | ------------- |
| Pydantic models | `models/`     |
| FastAPI routers | `api/`        |
| Business logic  | `services/`   |
| Utilities       | `utils/`      |
| Validation      | `validators/` |
| Logging config  | `logger/`     |
| Config loading  | `config/`     |

### Python file names

* Lowercase with underscores: `snake_case.py`
* Prefix with responsibility:

  * `model_`, `service_`, `validator_`, `helper_`, `config_`
* Examples:

  * `model_article.py`
  * `service_cart.py`
  * `helper_config_loader.py`

### `__init__.py` requirements

Each folder must contain a non-empty `__init__.py` file with:

* Header (`# File`, `# Path`)
* Description block as a docstring
* Optional logger initialization
* Optional default imports or base class exports

---

## 3. Logging Standards

* Use the built-in `logging` module
* Initialize with `logger = logging.getLogger(__name__)`

| Level   | Use Case                              |
| ------- | ------------------------------------- |
| DEBUG   | Validations, user inputs, state flows |
| INFO    | Lifecycle events, successful ops      |
| WARNING | Fallbacks, degraded modes             |
| ERROR   | Runtime errors                        |

Include contextual information in all log messages.

---

## 4. Typing Guidelines

* Use type hints on all functions and parameters

* Use `pydantic.BaseModel` for:

  * request/response schemas
  * structured config
  * return types

* Use `Literal`, `Annotated` or Enums for constrained values

---

## 5. Tooling

| Tool       | Purpose                     |
| ---------- | --------------------------- |
| `black`    | Auto-formatting             |
| `flake8`   | Linting (PEP8 + complexity) |
| `mypy`     | Static typing               |
| `pytest`   | Unit testing                |
| `coverage` | Optional coverage metrics   |

Run these tools via `Makefile`:

```bash
make format  # black
make lint    # flake8
make mypy    # type checking
make test    # pytest
```

---

## 6. Documentation Standards

* Every function and class must include a docstring:

  ```python
  ```

  # All files must end with the following marker:
  # EOF

  ```python
  def is_valid(article: str) -> bool:
      """Check if the article number is in the valid set.

      Args:
          article (str): The article number to validate.

      Returns:
          bool: True if valid, False otherwise.
      """
  ```

* Public classes must have a one-line summary and argument/return documentation

---

## 7. Exception Handling

* Avoid catching `Exception` unless absolutely necessary
* Define domain-specific exceptions in `exceptions.py`
* Use FastAPI’s `HTTPException` with proper status codes for API errors

---

## 8. Configuration Files

### Structure

All JSON config files must include a `_meta` field:

```json
{
  "_meta": {
    "description": "Config description",
    "usage": "What this config is for",
    "author": "Matthias Morath",
    "version": "1.0.0",
    "updated": "2025-07-18"
  },
  "data": { ... }
}
```

### Location & Naming

| Item          | Convention                         |
| ------------- | ---------------------------------- |
| Folder        | `config/`                          |
| Filename      | `config_<topic>.json`              |
| Loader module | `helpers/helper_config_<topic>.py` |
| Schema file   | `config/schema_<topic>.json`       |

### JSON Schema Validation

* Every config file must have a matching schema in `config/schema_*.json`
* Validation is done using `jsonschema.validate()`
* Raise `ValueError` or custom `ConfigValidationError` on failure

### Logging `_meta` info

Log this after successful load:

```text
[INFO] Loaded config_<topic>.json (vX.X.X) by <author> – <description>
```

### Testing

* All helpers must be tested under `tests/helpers/`
* Use fixture files in `tests/config/valid/` and `tests/config/invalid/`

```text
tests/config/
├── valid/
│   └── config_example_valid.json
└── invalid/
    └── config_example_invalid.json
```

---

## 9. Summary

All code must:

* Follow strict naming & folder conventions
* Include headers, logging, MARKs, and docstrings
* Use type safety and schema validation
* Ensure configs are self-documenting and testable
* Be verified via `black`, `flake8`, `mypy`, and `pytest`
