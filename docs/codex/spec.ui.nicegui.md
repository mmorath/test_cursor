# Ui.Nicegui

---
title: Ui.Nicegui
category: specification
status: active
last_updated: 1753967677.0033057
---

# Path: docs/spec.frontend.nicegui.md

# NiceGUI Frontend Specification

## 🎯 Zweck

Diese Spezifikation beschreibt die Struktur, Komponenten, Konventionen und Entwicklungsrichtlinien für Frontend-Anwendungen, die mit [NiceGUI](https://nicegui.io) entwickelt werden. Sie dient als Vorlage für modulare, wartbare und erweiterbare Anwendungen in Python.

---

## 📁 Projektstruktur

```text
app/
├── components/             # Wiederverwendbare UI-Komponenten (z. B. Input-Felder, Dialoge)
├── config/                 # Konfigurationsdateien und Umgebungsvariablen
├── helpers/                # Hilfsmodule (z. B. JSON-Loader, Ping-Services)
├── logger/                 # Logging-Initialisierung und Formatierung
├── models/                 # Pydantic-Datenmodelle für UI-Validierung und Konfiguration
├── routes/                 # Seitenrouting mittels @ui.page
├── services/               # Hintergrunddienste, MQTT, OPC UA, REST-Calls etc.
├── static/                 # Statische Assets wie CSS oder JS
├── templates/              # HTML-Templates, wenn nötig
├── validators/             # Eingabevalidierung als separate Funktionen/Module
├── views/                  # Visuelle Screens (Cards, Stepper, Dashboards)
└── main.py                 # Einstiegspunkt, Initialisierung, ui.run()
````

---

## 🔁 Komponenten-Prinzipien (`app/components`)

* Jede Komponente ist eine eigene Datei mit einem `create_<name>_step()` oder `create_<name>_component()`-Funktionsaufruf.
* Validierung erfolgt inline oder per `validators/`.
* Logging erfolgt auf Debug- oder Info-Level.
* UI-Rückgabe erfolgt immer über eine NiceGUI-Komponente (`ui.input`, `ui.select`, `ui.step`, etc.).

---

## 🧪 Validierung

* Validierungen sind entweder:

  * direkt im `validation={}` Attribut implementiert
  * ausgelagert in `validators/<domain>_validators.py`
* Regex-Prüfungen erfolgen über klar benannte Methoden (`validate_mac_address`, `validate_location_code` etc.)

---

## 🛠️ Konfigurationsprinzipien

* JSON-Dateien in `config/` dienen der UI-Konfiguration (z. B. Maschinenkataloge, Dropdown-Werte).
* Ladehilfen befinden sich in `helpers/helper_config_loader_*.py`.
* Pydantic-Modelle wie `model_machine_identification_code.py` sichern Struktur und Validität ab.

---

## 🔁 Views & Stepper (`app/views`)

* Views kapseln logische UI-Einheiten, z. B. Gerätekonfiguration oder Monitoring.
* Ein Stepper wird über `ui.stepper()` erstellt und durch `create_<name>_step()`-Funktionen befüllt.
* Zusammenfassungen nutzen `bind_content_from`.

---

## 🌐 Routing

* In `app/routes/routes.py` werden alle Seiten über `@ui.page()` definiert.
* Jede Seite sollte genau eine View-Komponente laden.
* Logging beim Aufruf jeder Route ist verpflichtend.
* Beispielroute siehe .

---

## 🧾 Logging-Konventionen

* Logger wird zentral in `logger/` initialisiert.
* In Komponenten & Views: `logger.info`, `logger.debug`, `logger.warning`
* Beispiel:

  ```python
  logger.info("Initialisiere Step: MAC-Adresse")
  ```

---

## ✅ Beispielkomponenten

Siehe  für ein vollständiges Beispiel mit Validierung, Logging und Stepper-Navigation.

---

## 🛠️ Entwicklungsumgebung

* Lokales Setup über `.venv` im Frontend-Verzeichnis
* Makefile-Kommandos für:

  * `install`
  * `run`
  * `clean`
  * `lint`, `format`, `mypy`, `test` optional

---

## 📘 Dokumentation

* Diese Spezifikation wird über `MkDocs` dargestellt (`mkdocs.yml`, Theme: `material`)
* Pfad im Repository: `docs/spec.frontend.nicegui.md`

---

## 📌 Empfehlung

* Strikte Trennung von Komponenten, Views, Routing
* Keine Logik in `main.py`, nur Initialisierung
* Reine UI-Logik in `views`, keine externe Abhängigkeiten laden
* Verwende `async` nur wenn absolut erforderlich in Komponenten (z. B. bei Service-Abfragen)

---

## 📦 Beispielabhängigkeiten (`requirements.in`)

```text
nicegui==1.4.20
pydantic==2.7.1
```

---

## 🧪 Tests

* UI-Komponenten werden über Smoke-Tests validiert
* `pytest` optional für Model-Validierung
* Beispieltest: `tests/test_model_machine_codes.py`

---

##
## 📋 Related Templates

- `components/input_validated_input.py.j2`
- `components/input_dropdown_select.py.j2`
- `routers/route_template_nicegui.py.j2`


## 📎 Lizenz

Dieses Template unterliegt der MIT-Lizenz.
