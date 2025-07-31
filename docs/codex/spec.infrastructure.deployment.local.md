# Infrastructure.Deployment.Local

---
title: Infrastructure.Deployment.Local
category: specification
status: active
last_updated: 1753967677.0033057
---

### 📄 `docs/codex/spec.deployment.local.md` (aktualisiert)

## Ziel
Diese Spezifikation beschreibt das lokale Deployment zweier unabhängiger Services – Backend (FastAPI) und Frontend (NiceGUI). Jeder Service erhält eine eigene virtuelle Umgebung. Die Abhängigkeiten werden ausschließlich über `requirements.in` gepflegt und mit `pip-compile` generiert.

---

## 📦 Verzeichnisstruktur

```text
supermarkt/
├── backend/
│   ├── app/
│   ├── .venv/                  # Virtuelle Umgebung für Backend
│   ├── requirements.in
│   └── requirements.txt       # Wird aus .in generiert
└── frontend/
    ├── app/
    ├── .venv/                  # Virtuelle Umgebung für Frontend
    ├── requirements.in
    └── requirements.txt       # Wird aus .in generiert
├── Makefile.native                 # Native Steuerung (optional)
└── docs/
    └── codex/
        └── spec.deployment.local.md
````

---

## 🧰 Voraussetzungen

* Python ≥ 3.11 (z. B. mit `pyenv`)
* `pip-tools` (z. B. via `pip install pip-tools`)
* keine Docker- oder Containerdienste erforderlich

---

## 🛠 Setup-Schritte (pro Service)

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
python3 -m venv .venv
source .venv/bin/activate
pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

**Hinweis:** Änderungen an Abhängigkeiten erfolgen **ausschließlich in `requirements.in`** – niemals direkt in `requirements.txt`.

---

## 🏃 Anwendung starten (nativ)

### Backend:

```bash
cd backend
source .venv/bin/activate
python app/main.py
```

### Frontend:

```bash
cd frontend
source .venv/bin/activate
python app/main.py
```

Oder kombiniert via:

```bash
make run  # Makefile.native muss dies unterstützen
```

---

## 🧼 Cleanup

```bash
make clean
```

Oder manuell:

```bash
rm -rf backend/.venv
rm -rf frontend/.venv
```

---

## 📁 .gitignore-Erweiterung

```gitignore
# Virtuelle Umgebungen
backend/.venv/
frontend/.venv/
```

---

## ✅ Best Practices

* `requirements.in` ist die einzige Quelle für Abhängigkeiten
* `pip-compile` generiert immer eine saubere, vollständige `requirements.txt`
* `.venv` ist projektspezifisch und versionsgebunden

---

## 📝 Autorenvermerk

> Erstellt von Matthias Morath
> Struktur für lokales Deployment mit sauberer Abhängigkeitsverwaltung und getrennter Umgebung pro Service.
