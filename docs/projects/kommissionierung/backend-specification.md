# Backend.Kommissionierung

---
title: Backend.Kommissionierung
category: specification
status: active
last_updated: 1753967677.0033057
---

## 📄 `spec.kommissionierung.backend.md`

### **Ziel**

Das Backend verwaltet den Kommissionierprozess projektbasiert. Es stellt eine REST-API für das Frontend bereit, verarbeitet Scans, speichert Fortschritt, erlaubt Fortsetzung bei Abbruch und publiziert Ereignisse an einen MQTT-basierten Event-Broker.

---

### **Hauptfunktionen**

* Authentifizierung via Username/Password (SSO optional)
* Laden & Validieren von Projekten anhand einer Projektnummer
* Zuweisung eines Materialwagens (per Scan)
* Auslesen der artikelspezifischen Pickingliste
* Verarbeiten von Artikel-Scans (inkl. Matching über Hersteller-Artikelnummer)
* Fortschrittsverwaltung (pro Artikel, pro Projekt, persistiert)
* Abschlusslogik mit Event-Publishing

---

### **Datenschema (DB / In-Memory Objekt)**

#### `Project`

```json
{
  "projekt_nr": "054516",
  "articles": [Article, ...],
  "status": "Offen" | "Komplett" | "In Bearbeitung",
  "startzeit": "...",
  "endzeit": "...",
  "letzter_kommissionierer": "user123"
}
```

#### `Article`

```json
{
  "artikel": "388303408",
  "artikel_bezeichnung": "...",
  "menge": 3,
  "einheit": "stk",
  "lagerplatz": "23IZ022A",
  "hersteller_artikelnummer": "XYZ-1234",
  "anzahl_auf_wagen": 1,
  "anzahl_fehlt": 1,
  "anzahl_beschaedigt": 0,
  "kommisionierer": "user123"
  ...
}
```

---

### **Referenzdatensatz**

Die Datei [`reference_dataset.csv`](../../data/reference_dataset.csv) enthält einen vollständigen Projektauftrag mit mehreren Artikelpositionen zur Kommissionierung. Sie dient als:

* 🧪 Testdatensatz für Validierungen
* 🔧 Grundlage für Modellierung und Persistenztests
* 📌 Referenz für reale Datenstruktur

---

### **REST-API Endpunkte**

#### `POST /auth/login`

* Authentifizierung via Benutzername/Passwort
* Response: JWT-Token oder Session-ID

#### `GET /project/{projekt_nr}`

* Validiert Projekt und liefert Metadaten + Artikelliste mit aktuellem Stand

#### `POST /project/{projekt_nr}/materialwagen`

* Koppelt einen Materialwagen zum Projekt

#### `POST /project/{projekt_nr}/scan`

* Body: `{ "artikelnummer": "388303408", "user": "user123" }`
* Validiert Eingabe gegen `artikel` oder `hersteller_artikelnummer`
* Erhöht `anzahl_auf_wagen`
* Response: Status (OK, Fehler, Menge erfüllt, nächster Artikel, …)

#### `POST /project/{projekt_nr}/artikel/{artikel}/status`

* Manuelles Markieren von:

  * `beschädigt` → `anzahl_beschaedigt += 1`
  * `nicht_vorhanden` → `anzahl_fehlt += 1`

#### `POST /project/{projekt_nr}/abschliessen`

* Prüft Vollständigkeit
* Publiziert `projekt_kommissioniert`-Event
* Markiert Projekt als abgeschlossen

---

### **MQTT Event: `projekt_kommissioniert`**

* Topic: `logistik/kommissionierung/abschluss/{projekt_nr}`
* Payload:

```json
{
  "projekt_nr": "054516",
  "articles_picked": [...],
  "articles_offen": [...]
}
```

---

### **Validierungslogik**

* Projektnummer = genau 6-stellig numerisch
* Materialwagen-ID = UUID, EAN oder numerisch
* Artikelnummer-Scan = `artikel` oder `hersteller_artikelnummer`
* Fortschritt wird **sofort persistiert** (z. B. SQLite, Postgres, Redis)

---

### **Spätere Erweiterungen (Platzhalter)**

* Trigger für Etikettendruck bei `anzahl_beschaedigt > 0`
* Trigger für Backorder bei `anzahl_fehlt > 0`
* SSO über AD/LDAP
* Multi-User-Protokollierung
