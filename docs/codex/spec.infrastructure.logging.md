# Infrastructure.Logging

---
title: Infrastructure.Logging
category: specification
status: active
last_updated: 1753967677.0033057
---

Das ist eine ausgezeichnete Idee, Matthias. Eine zentrale, konfigurierbare Logging-Spezifikation ist essenziell für:
	•	✅ Einheitliche Logs in Backend, CLI, Microservices etc.
	•	✅ Debugbarkeit & Monitoring, auch in Produktionsumgebungen (via ELK, Grafana Loki, etc.)
	•	✅ Anpassbarkeit, ohne Codeänderung – durch config.json

⸻

🔧 Vorschlag: spec.logging.md

Hier ist ein vollständiger Vorschlag für eine Codex-Spezifikation:

# Spezifikation: Logging-Konventionen und Konfiguration

## Zielsetzung

Ein konsistentes, konfigurierbares Logging-System ermöglicht sowohl während der Entwicklung als auch in Produktionsumgebungen eine klare Nachvollziehbarkeit aller Systemvorgänge.

Diese Spezifikation definiert:

- Logging-Formate
- Log-Level
- Konfigurierbarkeit via `config.logging.json`
- Strukturierte Log-Einträge
- Logging-Konventionen pro Modultyp (API, Service, CLI)

---

## 
## 📋 Related Templates

- `logger/logger_template.py.j2`
- `configs/config_logging.json.j2`


## 1. Logging-Konfiguration (`config/config_logging.json`)
*Vorlage: *

```json
{
  "version": 1,
  "disable_existing_loggers": false,
  "formatters": {
    "standard": {
      "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    },
    "detailed": {
      "format": "%(asctime)s | %(levelname)s | %(module)s.%(funcName)s:%(lineno)d | %(message)s"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "formatter": "standard",
      "level": "DEBUG"
    },
    "file": {
      "class": "logging.FileHandler",
      "filename": "logs/app.log",
      "formatter": "detailed",
      "level": "INFO"
    }
  },
  "root": {
    "handlers": ["console", "file"],
    "level": "DEBUG"
  }
}

💡 Die Konfiguration kann über ein Python-Modul wie load_logging_config() geladen werden.

⸻

2. Initialisierung

# Generiert aus 
Datei: app/logger/logger_config.py

# File: app/logger/logger_config.py
# -*- coding:utf-8 -*-
"""
Logging Initialisierung auf Basis von config/config_logging.json
"""

import logging.config
import json
from pathlib import Path

def init_logging(config_path: str = "config/config_logging.json"):
    """Initialisiert das globale Logging gemäß JSON-Konfiguration."""
    with open(config_path, "r") as f:
        config = json.load(f)
        logging.config.dictConfig(config)


⸻

3. Verwendung im Code

# Beispiel in route_project.py
import logging
logger = logging.getLogger(__name__)

logger.info("📦 Projekt erfolgreich geladen: %s", projekt_nr)
logger.warning("⚠️ Artikelanzahl nicht korrekt")
logger.error("❌ Fehler beim Speichern: %s", err)


⸻

4. Konventionen nach Typ

Bereich	Pflicht-Loglevel	Beschreibung
API-Calls	INFO	Methode, Route, Benutzer-ID, Request-Daten
Services	DEBUG/ERROR	Eingaben, Ausgaben, Validierungsfehler
CLI-Tools	INFO/ERROR	Schrittweiser Fortschritt, Ergebnisse
Validierung	WARNING	Ungültige Datenformate


⸻

5. Optional: Erweiterung mit Trace-ID / Request-ID

# Optional: Middleware für FastAPI
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    logging.getLogger("uvicorn.access").info("🆔 Request ID: %s", request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


⸻

📁 Ablage

docs/
└── codex/
    ├── spec.logging.md
    └── templates/
        ├── logger/logger_template.py.j2
        └── configs/config_template.json.j2


⸻