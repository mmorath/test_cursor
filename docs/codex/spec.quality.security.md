# Quality.Security

---
title: Quality.Security
category: specification
status: active
last_updated: 1753967677.0033057
---

Hier ist die vollständige Spezifikationsdatei `spec.security.md`, die du in deinem Projekt unter `docs/codex/` ablegen kannst:

---

````markdown
# File: spec.security.md
# Path: docs/codex/spec.security.md

# Spezifikation: Sicherheitsanforderungen und -maßnahmen

## 🎯 Ziel

Diese Spezifikation legt die zentralen Sicherheitsrichtlinien für alle Dienste des `supermarkt`-Projekts fest. Sie berücksichtigt Best Practices zur Absicherung von FastAPI-Backends, NiceGUI-Frontends, MQTT-Kommunikation und Infrastrukturkomponenten in lokalen und produktiven Umgebungen.

---

## 🔐 Allgemeine Sicherheitsprinzipien

- **Principle of Least Privilege (PoLP)** – Dienste, Container und Benutzer erhalten nur minimal notwendige Rechte.
- **Secure by Default** – Standardkonfigurationen sind restriktiv.
- **Defense in Depth** – Sicherheit wird auf mehreren Schichten implementiert (API, Netzwerk, Deployment).
- **Auditing & Logging** – Sicherheitsrelevante Ereignisse werden nachvollziehbar geloggt.

---

## 🧱 Backend (FastAPI)

### 🔐 Authentifizierung & Autorisierung

| Bereich       | Maßnahme |
|---------------|---------|
| Authentifizierung | JWT-basierte Tokens oder OAuth2 |
| Zugriffsschutz | Abgesicherte Routen via `Depends(get_current_user)` |
| Rollenmodell | Optional: `is_admin`, `is_operator`, etc. als Claims |

### 🔒 HTTP Security Header

- `Strict-Transport-Security`
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Content-Security-Policy`

### 🛡️ Schutz gegen Bedrohungen

| Bedrohung          | Maßnahme                             |
|--------------------|--------------------------------------|
| SQL-Injection      | ORM (z. B. SQLAlchemy) mit Parametrisierung |
| XSS / HTML-Injection | HTML-Escaping & CSP Header          |
| Rate Limiting      | z. B. mit `slowapi`                  |
| CSRF               | Bei Form-Interaktionen: CSRF-Tokens  |
| Directory Traversal | Validierte Pfadzugriffe             |

---

## 🌐 Frontend (NiceGUI)

| Aspekt               | Maßnahme                                   |
|----------------------|--------------------------------------------|
| Session Handling     | Kein lokaler Storage von Tokens im Browser |
| Eingabevalidierung   | Sowohl client- als auch serverseitig       |
| Logging              | Keine sensiblen Daten im Log (z. B. Tokens) |
| Zugriff              | Keine sensiblen Routen ohne Login anzeigen |
| Abgesicherte Kommunikation | HTTPS erzwingen, auch lokal über self-signed Zertifikate |

---

## 🔄 MQTT-Kommunikation

| Aspekt                | Maßnahme |
|-----------------------|----------|
| TLS/SSL               | Verwendung von Zertifikaten (`cafile`, `certfile`, `keyfile`) |
| Authentifizierung     | Username/Password oder mTLS-Clientzertifikate |
| ACL-Listen            | Nur erlaubte Topics publizieren/abonnieren |
| QoS-Konfiguration     | Nur notwendige QoS-Level verwenden (z. B. `QoS 1`) |
| Topic-Namespace       | Keine Wildcard-Subscriptions auf Root-Level (`#`) |

---

## 📁 Secrets & Konfiguration

| Bereich          | Maßnahme |
|------------------|----------|
| `.env`-Dateien   | Nie im Git tracked, über `.gitignore` ausgeschlossen |
| Secrets Management | Lokal: `.env`, Prod: Vault/Sealed Secrets (z. B. SOPS, Hashicorp Vault) |
| Docker Builds    | Keine Secrets in `Dockerfile` oder Layer-Caches |

---

## 🐳 Container-Sicherheit

| Bereich                  | Maßnahme |
|--------------------------|----------|
| Rootless Container       | Dienste laufen nicht als root |
| Read-Only Filesystem     | Wo möglich aktivieren |
| Minimalbaseimages        | z. B. `python:slim`, `distroless`, `alpine` |
| Image Signing/Scanning   | z. B. Trivy, Cosign, GitHub Dependabot Alerts |
| Automatisierte Updates   | Regelmäßiger Rebuild, Updatecheck via CI/CD |

---

## 🔒 Deployment & Infrastruktur

| Bereich                  | Maßnahme |
|--------------------------|----------|
| TLS überall              | Selbst in Testumgebungen erzwingen |
| Kubernetes Secrets       | Nur Base64, nie echte Verschlüsselung – ggf. externe Tools |
| Netzwerksegmentierung    | Services über NetworkPolicies absichern |
| Logging & Monitoring     | Sicherheitslogs getrennt speichern und auswerten |
| Audit Trails             | Besonders bei API-Zugriffen, Logins und Konfigurationsänderungen |

---

## 🔍 CI/CD Security

| Bereich                  | Maßnahme |
|--------------------------|----------|
| Secrets in Actions       | Verwendung von GitHub Secrets (kein plaintext) |
| Dependency Audits        | z. B. `pip-audit`, `safety`, `npm audit`, `cargo audit` |
| Commit-Linter            | Kein accidental Secrets (`detect-secrets`, `gitleaks`) |
| CI-Runner Hardening      | Keine unnötigen Tools auf CI-Runtime-Image |

---

## 📜 Beispiel: `.env` Absicherung

```bash
# File: .gitignore
.env
.env.*
secrets/
*.pem
````

---

## ✅ Checkliste für Sicherheitsreview

* [ ] Sind sensible Routen durch Auth abgesichert?
* [ ] Werden API-Parameter validiert?
* [ ] Enthält das Image unnötige Tools?
* [ ] Sind alle Secrets nur in `.env` oder im Secret Manager?
* [ ] Ist HTTPS aktiv – auch in der lokalen Umgebung?
* [ ] Gibt es Logging für verdächtige Anfragen?
* [ ] Werden Container regelmäßig rebuilt und gescannt?

---

## 📘 Referenzen

* [OWASP Top 10](https://owasp.org/www-project-top-ten/)
* [FastAPI Security Guide](https://fastapi.tiangolo.com/advanced/security/)
* [Mozilla Secure Headers](https://infosec.mozilla.org/guidelines/web_security.html)
* [MQTT Security Best Practices (HiveMQ)](https://www.hivemq.com/mqtt-security-fundamentals/)

```