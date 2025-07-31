# Project.Kommissionierung.Overview

---
title: Project.Kommissionierung.Overview
category: specification
status: active
last_updated: 1753967677.0033057
---

## 📄 `spec.kommissionierung.overview.md`

# 📄 Produktspezifikation: Kommissionier-App für Projektmaterial

## Zielsetzung

Die Anwendung unterstützt Werksmitarbeiter beim kompakten, scanbasierten Kommissionieren von Materialien zu Baugruppen eines Projekts. Sie stellt sicher, dass:

* Projekte anhand von Projekt-IDs eindeutig identifiziert werden,
* Materialwagen korrekt zugeordnet werden,
* Artikel nach einem festen Plan und in richtiger Menge gepickt werden,
* Fortschritt sichtbar ist und Fehler vermieden werden,
* Picking-Vorgänge jederzeit fortgesetzt werden können,
* das ERP-System via MQTT Event informiert wird.

## Zielnutzer

* Kommissionierer (Standardrolle)
* Privilegierter Kommissionierer (für zukünftige Erweiterungen: z. B. Stornos)

## Ablauf

1. Login via Username/Password
2. Projekt-Nr. Eingabe/Scan → Validierung durch Backend
3. Materialwagen-Scan → Zuordnung im Backend
4. Schrittweises Picking:

   * Anzeige von Artikelinformationen (Artikelnummer, Bezeichnung, Menge, Einheit, Lagerplatz)
   * Scan von Artikelnummer (intern `artikel` oder Hersteller `hersteller_artikelnummer`)
   * Feedback:

     * Korrekt: akustischer Ton, Fortschrittsanzeige aktualisiert, grünes UI-Feedback
     * Falsch: rotes Eingabefeld, Fehlermeldung
   * Fortschrittsanzeige: z. B. "2 von 3 gescannt"
   * Wenn `anzahl_auf_wagen == menge` → nächster Artikel
5. Abschlussseite nach letztem Pick: Meldung "Kommissionierung abgeschlossen"
6. MQTT-Event `projekt_kommissioniert` inkl. aller relevanten Daten

## Technische Rahmenbedingungen

* Backend: FastAPI
* Frontend: NiceGUI
* Datenquelle: CSV beim Start eingelesen und normalisiert
* Event-Dispatch: MQTT-basierter Enterprise-Broker
* Später: Wireless-Druckintegration für QA- oder Backorder-Etiketten

## Persistenz & Fortführung

* Picking-Prozess ist persistent
* Jeder Pick wird mit Benutzer-ID gespeichert (`kommisionierer`)
* Projekt kann von anderen Nutzern fortgeführt werden
* Felder zur Erfassung von Abweichungen:

  * `anzahl_auf_wagen`
  * `anzahl_fehlt`
  * `anzahl_beschaedigt`
  * `kommisionierer`

## Eventstruktur

MQTT-Topic: `logistik/kommissionierung/abschluss/<projekt_nr>`
Payload:

```json
{
  "projekt_nr": "054516",
  "articles_picked": [
    {
      "artikel": "...",
      "artikel_bezeichnung": "...",
      "menge": 3,
      "anzahl_auf_wagen": 3,
      "anzahl_fehlt": 0,
      "anzahl_beschaedigt": 0,
      "kommisionierer": "user123"
    }
  ],
  "articles_offen": [
    {
      "artikel": "...",
      "artikel_bezeichnung": "...",
      "menge": 2,
      "anzahl_auf_wagen": 1
    }
  ]
}
```

---