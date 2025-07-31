# Quality.Vcs

---
title: Quality.Vcs
category: specification
status: active
last_updated: 1753967677.0033057
---

# Spezifikation: VCS Hygiene

Diese kurze Spezifikation definiert Mindestanforderungen an die Versionsverwaltung.

## Commit-Richtlinien

- Aussagekräftige Commit-Botschaften im Imperativ
- Kleine, thematische Commits anstelle großer Sammeländerungen
- Verweise auf Issues oder Spezifikationen, sofern vorhanden

## Branch-Naming

- Feature-Branches: `feature/<kurzbeschreibung>`
- Bugfix-Branches: `fix/<issue-id>`
- Dokumentation: `docs/<bereich>`

## Pull Requests

- Jeder Branch wird über einen Pull Request gemerged
- Beschreibung muss Zweck und Änderungen zusammenfassen
- Mindestens eine Review erforderlich

