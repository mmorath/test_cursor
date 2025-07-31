# Backend.Api.Conventions

---
title: Backend.Api.Conventions
category: specification
status: active
last_updated: 1753967677.0033057
---

# 📄 `docs/codex/spec.api_conventions.md`

**API Design & Response Conventions**

Diese Spezifikation definiert verbindliche Regeln für alle FastAPI-basierten APIs im Projekt. Sie stellt sicher, dass alle Schnittstellen versioniert, konsistent dokumentiert, strukturiert getestet und maschinen- wie menschenlesbar sind.

---

## 1. API-Versionierung & Basisstruktur

* Alle Endpunkte müssen unter einem versionierten Pfad beginnen:
  `api/v1/...`
* Zukünftige Breaking Changes werden über `v2/`, `v3/` eingeführt.
* FastAPI-Router verwenden den `prefix`-Parameter:

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/cart",
    tags=["Cart"]
)
```

---

## 2. Pfadkonventionen & Namensregeln

* **Ressourcen im Plural** benennen: `/projects`, `/articles`, `/users`
* **Subressourcen mit Bindestrich**: `/order-items`, `/picking-status`
* **Keine Verben in Pfaden**: Statt `/checkCart`, lieber `POST /cart/validate`
* IDs gehören in den Pfad: `/articles/{article_id}`

---

## 3. HTTP-Statuscodes

| Fall                            | Methode | Code               |
| ------------------------------- | ------- | ------------------ |
| Erfolgreicher Abruf             | GET     | 200 OK             |
| Ressource erstellt              | POST    | 201 Created        |
| Erfolgreich gelöscht            | DELETE  | 204 No Content     |
| Ungültige Anfrage / Validierung | \*      | 400 Bad Request    |
| Nicht authentifiziert           | \*      | 401 Unauthorized   |
| Nicht berechtigt                | \*      | 403 Forbidden      |
| Nicht gefunden                  | \*      | 404 Not Found      |
| Konflikt (z. B. Duplikat)       | \*      | 409 Conflict       |
| Serverfehler                    | \*      | 500 Internal Error |

---

## 4. Einheitliches Response-Wrapping

Alle Antworten (Erfolg & Fehler) folgen diesem Schema:

```json
{
  "success": true,
  "data": {...},
  "error": null
}
```

Bei Fehlern:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_CART",
    "message": "Der Warenkorb konnte nicht validiert werden",
    "details": {
      "missing_fields": ["articleNumber"]
    }
  }
}
```

---

## 5. Fehlerstruktur (`ErrorModel`)

```python
from pydantic import BaseModel
from typing import Optional

class ErrorModel(BaseModel):
    code: str                     # Maschinenlesbar, z. B. "INVALID_CART"
    message: str                  # Für Benutzer verständlich
    details: Optional[dict] = None  # Optional: Kontext (z. B. fehlende Felder)
```

Jeder Fehler muss einen `code` und eine beschreibende `message` enthalten.

---

## 6. Erfolgsstruktur (`ResponseModel`)

```python
from typing import TypeVar, Generic, Optional, Literal
from pydantic import BaseModel

T = TypeVar("T")

class ResponseModel(Generic[T], BaseModel):
    success: Literal[True]
    data: T
    error: None = None
```

Für Fehler wird ergänzend verwendet:

```python
class ErrorResponse(BaseModel):
    success: Literal[False]
    data: None = None
    error: ErrorModel
```

In der Route als Union zurückgeben:

```python
@router.post("/validate", response_model=Union[ResponseModel[CartValidated], ErrorResponse])
def validate_cart(...): ...
```

---

## 7. FastAPI Routing-Konventionen

* Jeder Endpoint muss:

  * `status_code=...` angeben
  * `response_model=...` definieren
  * `response_model_exclude_unset=True` setzen
* Verwende `tags`, `summary`, `description`:

```python
@router.get(
    "/status",
    response_model=ResponseModel[StatusModel],
    response_model_exclude_unset=True,
    status_code=200,
    tags=["Picking"],
    summary="Picking-Status abrufen",
    description="Gibt den aktuellen Status des Pick-Vorgangs zurück."
)
def get_status():
    ...
```

---

## 8. Pydantic für alle Rückgaben

* Alle Rückgaben **müssen** ein Pydantic-Modell sein
* Niemals nackte `dict`, `list`, `str`, `tuple` zurückgeben
* FastAPI validiert automatisch gegen das `response_model`

---

## 9. OpenAPI / Schema-Dokumentation

* Alle Felder, Models, Routen und Parameter müssen automatisch dokumentierbar sein
* Keine unbekannten Felder (verwende `extra = \"forbid\"` bei Modellen)
* Keine internen Fehlerstrukturen nach außen geben (z. B. keine Tracebacks)

---

## 10. Tests

* Jeder API-Endpunkt muss mindestens **drei** Tests haben:

  1. Gültiger Input → Erfolg
  2. Ungültiger Input → Fehler (422/400)
  3. Berechtigungsfehler → 401/403

* Struktur:

```text
tests/
└── api/
    ├── test_cart_validate.py
    └── test_auth_login.py
```

* Response-Wrapper und Fehlercode müssen mitgeprüft werden.


