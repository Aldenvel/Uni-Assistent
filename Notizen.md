Daten für User bereitlegen/Dummy-Daten

Sicherheitsbackup erstellen vom Projekt

Dockercontainer für Ollama?

Stichwort Docker Modelrunnner

Moounten von Uni und Ollama


Abgabetemplate; 


Systemprompt-Rolle: Antworten nur anhand der Daten)=KI
User-Prompt= Prompt den wir eingeben.Zouia Alkurdi, an Alle, response = ollama.chat( model=modell_name, messages=[ { "role": "system", "content": ( "Du bist ein Assistent, der Fragen ausschließlich auf Grundlage des bereitgestellten Kontextes beantwortet. " "Wenn die Antwort nicht eindeutig im Kontext steht, antworte exakt mit: NOT_FOUND. " "Füge keine weiteren Informationen hinzu." ), }, { "role": "user", "content": _build_prompt(frage, kontext_text), }, ],, 16:40,
Zu einem Eintrag gelangen Sie mit den Pfeiltasten.


Kubernetis bis Samstag implementieren: 2 Service und 2 Deployment Dateien, einmal für Core und einmal für Ollama. Config-map.

---
## 2025-11-10 Technische Anforderungen – Gap Analyse & Maßnahmen

### 1. AI-Komponente (Anforderung)
Aktueller Stand:
- Implementiert: RAG-Fragenbeantwortung (Kontextsuche mit FAISS + Ollama), Quiz-Generator, Wiederholung.
- Verlässlichkeit: Basis vorhanden (Standardantwort bei fehlendem Kontext, strikte Validierung in `rag_engine.py`).

Fehlend / Verbesserungen:
- Explizite Funktion "Zusammenfassung" oder "Empfehlung" als zusätzliche AI-Funktion (für Mindestanforderung klarer ausgewiesen).
- Standardantwort vereinheitlichen auf kurze Form: "Ich weiß es nicht" (statt verschiedene Varianten) – Konsistenz.
- Logging einer KI-Antwort mit Flag, ob Kontext ausreichend war (für Transparenz/Ethik Abschnitt).
- Optional: Einbindung externer API (OpenAI/Deepseek) als alternative Modellquelle – austauschbar über ENV.

Maßnahmen:
- Neue Route `/api/zusammenfassung/<fach>`: Nimmt Text oder Dateiname, liefert kurze Zusammenfassung (Systemprompt begrenzt Tokens, fallback bei Leere).
- Abstraktionsschicht `core/model_gateway.py` erstellen: wählt Ollama oder OpenAI basierend auf ENV `MODEL_PROVIDER`.
- Vereinheitlichung Rückgabetext in `ollama_interface.py` & `rag_engine.py` auf exakt: "Ich weiß es nicht".
- Audit-Log (CSV oder JSONL unter `data/audit/`) mit Feldern: `timestamp, fach, frage, kontext_tokens, answered, source_model`.

### 2. Docker (Anforderung)
Aktueller Stand:
- Containerisierung vorhanden, gehärtetes Dockerfile, Non-Root, getrennte Volumes, read-only Root-FS.
- Compose: Web + Ollama Services vorhanden.

Fehlend / Verbesserungen:
- Healthcheck Endpoint + Compose Healthcheck.
- Explizite Dokumentation im README zu Sicherheitsmaßnahmen.
- Multi-Stage Build optional zur weiteren Schlankheit (momentan okay – optional).

Maßnahmen:
- `/healthz` Route in `app.py` (returns JSON `{"status":"ok"}`) + `healthcheck:` Block in compose.
- README Abschnitt "Sicherheit & Betrieb" ergänzen.
- Optionaler Wechsel zu Multi-Stage Build (nur wenn Image-Größe kritisch).

### 3. Kubernetes (Anforderung)
Aktueller Stand:
- Noch nicht umgesetzt; Notiz erwähnt 2 Services + 2 Deployments.

Zielarchitektur (lokal mit kind):
- Namespace: `uni-assistent`.
- Deployments: `web-deployment`, `ollama-deployment` (ggf. StatefulSet für Modellpersistenz).
- Services: `web-svc` (ClusterIP), `ollama-svc` (ClusterIP).
- ConfigMap: `app-config` (MODEL_PROVIDER, DEFAULT_FACH optional).
- Secret (optional für API Keys zukünftiger externer Provider).
- Ingress (nur wenn externe UI gewünscht – laut Anforderung eigentlich nur API nötig → weglassen oder später).

Fehlend / Verbesserungen:
- Erstellung Ordner `k8s/` mit: `namespace.yaml`, `configmap.yaml`, `deployment-web.yaml`, `deployment-ollama.yaml`, `service-web.yaml`, `service-ollama.yaml`.
- README Kurzanleitung: `kind create cluster` + `kubectl apply -f k8s/`.

Maßnahmen:
- Minimalistische API-Version der App (reine JSON-Routen) zusätzlich zu HTML? → Anforderung sagt "nur API-Endpunkte notwendig"; Option: separate Flask Blueprint `api.py` mit `/api/frage` & `/api/zusammenfassung`.
- Ressourcenlimits in Deployments spiegeln Compose.

### 4. Ergänzende Punkte für Bewertung
- Pitch: Check-Liste für Vorbereitung (Script, Kernnutzen, Technik Kurzinfo, Verlässlichkeit der Antworten betonen).
- Ethik/Transparenz: Im README dokumentieren: Datenquellen sind lokale Kursunterlagen; KI halluziniert nicht dank striktem Kontextfilter; Fallback "Ich weiß es nicht".
- Zukunftsvision: Hinweis auf Erweiterung durch Lernfortschrittsadaptives Scheduling & Multi-Model-Unterstützung.

### 5. Konkrete Nächste Schritte (Priorisiert)
1. Healthcheck Endpoint & Compose Healthcheck.
2. Einheitlicher Fallback-Text implementieren.
3. Zusammenfassungs-API + Model-Gateway.
4. Audit-Log integrieren.
5. Ordner `k8s/` mit Basismanifeste erzeugen.
6. README erweitern (Architektur, Sicherheit, Deployment Schritte).
7. Pitch aufnehmen.

### 6. Aufwandsschätzung (grob)
- Healthcheck / Fallback: ~30 Min
- Zusammenfassung + Gateway: ~1–1.5 h
- Audit-Log: ~30 Min
- K8s Manifeste: ~1 h
- README Ergänzungen: ~45 Min
- Pitch: ~30–45 Min Vorbereitung & Aufnahme

### 7. Risiken / Aufmerksamkeit
- Modell-Latenz bei Zusammenfassung → evtl. Kürzere Chunk-Länge oder Token-Limit.
- Kubernetes lokal: Ressourcenverbrauch durch Ollama; ggf. Node-Memory erhöhen.
- Einheitlicher Fallback muss überall konsistent (Quiz/Frage/Editor) – prüfen alle Stellen.

---
Ende Eintrag.