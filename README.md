# Uni-Assistent – AI-gestützter Lernbegleiter
## 1. Executive Summary
Der Uni-Assistent ist ein lokal ausführbarer, datenschutzorientierter Lernbegleiter, der Studierende beim gezielten Verständnis ihrer Vorlesungsunterlagen unterstützt.
Er kombiniert Retrieval‑Augmented Generation (RAG) mit lokalem Modell‑Serving (Ollama + Mistral) und einer semantischen Vektorsuche (FAISS).
Ziel ist eine präzise, quellennachweisfähige Antwort auf fachliche Fragen, ohne auf externe LLM‑APIs zugreifen zu müssen.
Die Benutzeroberfläche ist barrierefrei gestaltet (WCAG 2.2 AA) und bietet interaktive Funktionen wie Quiz‑/Karteikarten‑Erstellung und Wiederholungs‑Workflows.
Das Projekt ist als praktischer Prototyp konzipiert, um Forschungsergebnisse und Lehrinhalte lokal nutzbar zu machen.
Es ermöglicht einfache lokale Nutzung via Docker Compose sowie eine skalierbare Ausführung in Kubernetes‑Umgebungen.
Diese README beschreibt Nutzung, Architektur, Sicherheitsüberlegungen und Wege zur Skalierung für mehrere Nutzer.
## 2. Ziele des Projekts
Verbessern der Lernqualität durch schnellen, kontextbasierten Zugriff auf Vorlesungsinhalte und Reduktion von Suchaufwand.
Ermöglichen inklusiver Lernzugänge durch Accessibility‑Features, die Screenreader und Tastaturnutzung unterstützen.
Minimieren von Halluzinationen: Antworten basieren ausschließlich auf den bereitgestellten Dokumenten und werden mit Quellen versehen.
Schutz sensibler Materialien: lokale Ausführung vermeidet das Hochladen persönlicher Unterlagen in die Cloud.
Bereitstellen eines erweiterbaren Prototyps für Forschung und Lehre, der als Grundlage für produktive Systeme dienen kann.
Dokumentation und Automatisierung (Docker/K8s) vereinfachen Wiederholbarkeit und Demonstrationen in Lehrkontexten.
Favorisieren modularer Architektur, damit Komponenten (Search, Embeddings, Inference) unabhängig skaliert werden können.
## 3. Anwendung und Nutzung
Benutzer konfigurieren einen lokalen Ordner mit Vorlesungsmaterialien, der von der App indiziert wird (Ordnerstruktur pro Fach).
Im Browser wählt man ein Fach, stellt eine Frage und erhält eine Antwort mit direkten Quellenverweisen auf Textstellen.
Die UI unterstützt außerdem das Erzeugen von Karteikarten (Multiple‑Choice, Freitext, Wahr/Falsch) zur Wiederholung.
Für Entwickler gibt es eine JSON‑API (`/api/frage/<fach>`) zur Integration in andere Tools oder für automatisierte Tests.
Für lange Modellläufe zeigt die UI einen WCAG‑konformen Lade‑Dialog mit Spinner, Progressbar und Abbrechen‑Funktion.
Administratoren können die App lokal via `docker compose up` oder in Kubernetes deployen (k8s/ Manifeste im Repo).
Die Befehlsdokumentation (`Befehle.md`) enthält gängige Operationen wie Logs‑Check, Port‑Forward und Modell‑Management.
## 4. Entwicklungsstand
Funktionaler Prototyp: Dokumenten‑Ingestion, Embedding‑Generierung, FAISS‑Indexing und RAG‑Pipeline sind implementiert.
Ollama‑Integration (Mistral) ist eingerichtet; es existiert ein Init‑Mechanismus zum automatischen Modell‑Pull beim Start.
Warmup‑Skript lädt SentenceTransformer vor Flask‑Start, um Cold‑Start‑Timeouts zu vermeiden.
Accessibility‑Features sind implementiert (aria‑Attribute, focus management, live regions) — manuelle Nutzertests empfohlen.
Kubernetes‑Manifeste mit Ressourcen‑Requests/Limits und HealthChecks sind im `k8s/`‑Ordner enthalten.
Dokumentation (Hilfe‑Doku, Befehle) ist vorhanden; Tests und Monitoring sind als nächste Schritte geplant.
Für produktiven Betrieb fehlen Authentifizierung, Rate‑Limiting und ein robustes Backup‑/Restore‑Konzept für Indizes.
## 5. Projektdetails
Dokumente werden in kleinere Chunks zerlegt, geembeddet (SentenceTransformers) und in einem lokalen FAISS‑Index gespeichert.
Die RAG‑Pipeline wählt relevante Chunks, baut einen stark kontextgebundenen Prompt und fragt das lokale Modell via Ollama an.
Antworten enthalten eine Quellenliste mit Dateiname und Textausschnitt, damit Nutzer die Herkunft verifizieren können.
Der Workflow ist bewusst modular: Indexing, Search und Inference sind separierbar und austauschbar.
Caching verhindert wiederholte Embedding‑Berechnungen; `data/cache` hält Embeddings und Indexdaten persistiert.
Fehlende oder unzureichende Kontexttreffer führen zu einer definierten Fallback‑Antwort, um Halluzinationen zu reduzieren.
Das Repository enthält außerdem Werkzeuge zur Demo‑Daten‑Erzeugung und zum Reset des Indexes für Tests.
## 6. Innovation
Verknüpfung von RAG‑Techniken mit strengen Accessibility‑Richtlinien ist ungewöhnlich und erhöht den Praxisnutzen.
Lokales Modell‑Serving (Ollama) kombiniert Datenschutz mit guter Latenz gegenüber Cloud‑APIs, solange Ressourcen verfügbar sind.
Warmup‑Pattern für ML‑Modelle minimiert HealthCheck‑Timeouts in orchestrierten Umgebungen.
Die explizite Fallback‑Strategie reduziert Fehlinformationen und macht Antworten nachvollziehbar.
Einfache Deployment‑Muster (Docker Compose + K8s Manifeste) erleichtern Reproduzierbarkeit in Lehr‑ und Demo‑Szenarios.
Modularität erlaubt späteren Einsatz von spezialisierten Vektor‑DBs, Model‑Serving oder GPU‑Nodes.
Das Projekt ist als Lehr‑ und Forschungsbasis gedacht, die direkt in Kurse integrierbar ist.
## 7. Wirkung (Impact)
Ermöglicht Studierenden schnellen Zugriff auf relevante Stellen in ihren Unterlagen und reduziert Zeitverlust beim Suchen.
Fördert wissenschaftliches Arbeiten durch transparente Quellenangaben und überprüfbare Antworten.
Unterstützt inklusive Lehre durch bewusste UI‑Entscheidungen (Screenreader, Tastaturnavigation, Farben mit hohem Kontrast).
Schützt sensible Lernmaterialien, da keine externen APIs für die eigentliche Inferenz genutzt werden müssen.
Bietet Lehrenden ein Werkzeug zur Erstellung adaptiver Quizsets und zur Automatisierung von Übungsfragen.
Ermöglicht Forschung zu RAG‑Methoden, besten Praktiken für lokale Inference und Accessibility‑Optimierungen.
Skalierbare Architektur‑Entwürfe erlauben künftige Integration in Hochschul‑IT‑Landschaften.
## 8. Technische Exzellenz
Sprache: Python 3.12 – breite ML‑Ökosystem‑Unterstützung; einfache Integration von Transformers und FAISS.
Web: Prototyp mit Flask; empfohlen: Migration zu FastAPI für asynchrone I/O‑Lasten und bessere Skalierbarkeit.
Embeddings: `all‑MiniLM‑L6‑v2` für guten Kompromiss aus Genauigkeit, Speed und Speicherbedarf.
Search: FAISS lokal für niedrige Latenz; Option: Weaviate/Milvus als verwaltete Alternative bei hohem Nutzungsgrad.
Model‑Serving: Ollama + Mistral lokal — gute Privacy; in Produktion: dedizierte Inference‑Pods oder spezialisierte Server.
CI/CD & Security: Image‑Scanning, Dependabot‑Prüfungen, Secrets in K8s Secrets, TLS via Ingress + cert‑manager empfohlen.
Observability: Prometheus/Grafana + zentrale Logs (Loki) + Tracing (OpenTelemetry) für Debugging und SLOs.
## 9. Ethik, Transparenz und Inklusion
Antihalluzinations‑Strategie: Bei mangelndem Kontext wird eine standardisierte Fallback‑Antwort ausgegeben.
Quellentransparenz: Jede generierte Antwort listet die verwendeten Dokumente und Textabschnitte auf.
Datenschutz: Lokale Verarbeitung verhindert Übertragung sensibler Inhalte in die Cloud.
Inklusion: WCAG 2.2 AA Features sind integraler Bestandteil des UI‑Designs.
Offenlegung: Informationen über Trainingsdaten oder Modell‑Bias werden dokumentiert; Nutzer werden auf mögliche Limitationen hingewiesen.
Ethische Richtlinien sollten bei produktiver Nutzung um Audit‑Logs, Moderation und Nutzungsrichtlinien erweitert werden.
Zukünftige Arbeit: Nutzertests mit diversen Zielgruppen zur Validierung der Accessibility‑Annahmen.
## 10. Zukunftsvision & Roadmap
Kurzfristig: Auth (OAuth2/JWT), Job‑Queue (Redis + Celery/RQ) für asynchrone Inferenz, Backup für Indizes.
Mittelfristig: Migration zu FastAPI, Externalisierung des Model‑Serving, Einsatz verwalteter Vektor‑DBs.
Infrastruktur: K8s Produktion mit HPA, Ingress (TLS), NodePools für inference‑workloads (CPU/GPU).
Funktional: Multimodale Ingestion (Audio/Video), fine‑tuning für Fachgebiete, kollaborative Notizen/Sharing.
Geschäftlich: Lizenzierbare Variante für Bildungseinrichtungen, Integrationen zu LMS (Moodle) und Single‑Sign‑On.
Langfristig: Adaptive Lehrpfade, personalisierte Review‑Algorithmen (Spaced Repetition) und APIs für Drittanbieter.
Roadmap & Issues: TODO‑Liste und Issues im GitHub‑Repository dokumentieren Prioritäten und Verantwortlichkeiten.
---
## Installation & Schnellstart
1) Lokale Entwicklung mit Docker Compose:
```powershell
docker compose build --no-cache
docker compose up -d
```
2) Browser: `http://localhost:5000` → Setup → Pfad zu deinen Uni‑Dokumenten angeben.
3) K8s: Ressourcen im `k8s/` Ordner anwenden; InitContainer lädt Modell automatisch beim ersten Start.
4) Wichtige Befehle: siehe `Befehle.md` für Logs, Port‑Forward und Modell‑Management.
5) Hinweise: Docker Desktop RAM mindestens 16GB empfohlen für Mistral; Index‑Speicher in `data/cache`.
---
## Beitrag & Entwicklung
Contributions sind willkommen: Issues für Bugs, Feature‑Requests oder Verbesserungen öffnen.
Coding‑Standards: Python 3.12, type hints, linters (flake8/ruff) und black formatting empfohlen.
Vor dem PR: Tests lokal ausführen, Formatierung prüfen und kurze Beschreibung hinzufügen.
Sensitive data: Keine privaten Dokumente in PRs posten; Beispiel‑Daten sind im Demo‑Config‑Set enthalten.
CI: GitHub Actions können hinzugefügt werden für Tests, Linting und Image‑Builds.
Roadmap und größere Änderungen bitte als Issue + Design Proposal anlegen.
---
**Autor:** Aleksandar Deniz Veljkovic
**Datum:** 15. November 2025
**Kontakt:** aleksandar.veljkovic@student.htw-berlin.de
# Uni-Assistent – AI-gestützter Lernbegleiter

## 1. Executive Summary

Der Uni-Assistent ist ein intelligenter Lernbegleiter, der Studierenden hilft, ihre Vorlesungsmaterialien besser zu verstehen und effektiver zu lernen. Das System verwendet Retrieval-Augmented Generation (RAG) in Kombination mit einem lokalen Sprachmodell (Mistral via Ollama), um präzise Antworten auf Fragen zu Studieninhalten zu liefern. Die Anwendung läuft vollständig lokal in Docker-Containern und kann über Kubernetes orchestriert werden. Besonders hervorzuheben ist die barrierefreie Benutzeroberfläche nach WCAG 2.2 AA Standard, die allen Studierenden – unabhängig von individuellen Einschränkungen – gleichberechtigten Zugang ermöglichen soll. Das System analysiert hochgeladene Dokumente, erstellt einen Vektorindex und beantwortet dann spezifische Fragen unter Angabe der verwendeten Quellen. Zudem enthält der Uni-Assistent die Möglichkeit selbst oder mit Hilfe der KI Karteikarten zur Prüfungsvorbereitung zu erstellen, dabei gibt es verschiedene Stile (Multiple-Coice, Freitext, Wahr-/Falsch-Aussagen). Die Quize/KArteikarten sind mit einem Punktesystem implementiert, bei dem der reiz des lernens durch Wiederholung spielerisch behandelt wird.

## 2. Ziele des Projekts

Das Hauptziel des Uni-Assistenten ist es, die Lerneffizienz von Studierenden zu steigern und gleichzeitig Barrieren beim Zugang zu Bildungsinhalten abzubauen. Viele Studierende kämpfen mit der Menge an Vorlesungsmaterialien und haben Schwierigkeiten, relevante Informationen schnell zu finden oder komplexe Zusammenhänge zu verstehen. Der Uni-Assistent löst dieses Problem, indem er als intelligenter Ansprechpartner fungiert, der rund um die Uhr verfügbar ist und maßgeschneiderte Antworten auf individuelle Fragen liefert. Dabei werden ausschließlich die eigenen Studienmaterialien als Wissensquelle verwendet, was Halluzinationen minimiert und die Verlässlichkeit der Antworten maximiert. Ein weiteres wichtiges Ziel ist die Inklusion: Durch die Implementierung von WCAG 2.2 AA Accessibility-Features können auch Studierende mit Sehbehinderungen oder motorischen Einschränkungen das System vollständig nutzen.

## 3. Anwendung und Nutzung

Der Uni-Assistent richtet sich primär an Studierende aller Fachrichtungen, die ihre Lernmaterialien digital vorliegen haben. Die Nutzung erfolgt über eine webbasierte Oberfläche: Studierende hinterlegen den Pfad zu Ihren Vorlesungsskripten, PDFs oder Textdokumente hoch und organisieren diese nach Fächern. Anschließend können sie natürlichsprachige Fragen stellen wie „Was ist Docker?" oder „Erkläre den Unterschied zwischen Pods und Deployments in Kubernetes". Das System durchsucht die relevanten Dokumente semantisch, findet die passendsten Textpassagen und generiert eine fundierte Antwort unter Angabe der Quellen. Die barrierefreie Oberfläche mit Screenreader-Unterstützung, Tastaturnavigation und visuellen sowie semantischen Fortschrittsanzeigen ermöglicht auch Studierenden mit Behinderungen eine selbstständige Nutzung.

**Code-Repository:** https://github.com/Aldenvel/Uni-Assistent  
**Pitch:** Die mp3 wurde per Mail übersendet.

## 4. Entwicklungsstand

Das Projekt befindet sich im Status eines **funktionsfähigen Prototyps**. Alle Kernfunktionen sind implementiert und getestet: Die RAG-Pipeline funktioniert zuverlässig, die Vektorsuche liefert relevante Ergebnisse, und das Ollama-Modell generiert präzise Antworten basierend auf den Quelldokumenten. Die Docker-Containerisierung ist abgeschlossen, und die Kubernetes-Deployments mit zwei Services (uni-app und ollama) laufen stabil. Die barrierefreie Benutzeroberfläche wurde nach WCAG 2.2 AA Richtlinien implementiert und umfasst alle erforderlichen ARIA-Attribute, Fokus-Management und alternative Texte. Der Prototyp ist bereits einsatzbereit für den persönlichen Gebrauch und könnte mit weiteren Features wie Nutzerauthentifizierung, Cloud-Deployment und Multi-User-Support zur produktionsreifen Anwendung weiterentwickelt werden.

## 5. Projektdetails

Der Uni-Assistent bietet mehrere Kernfunktionen: **Dokumenten-Integration und -Verwaltung (Cashe)** ermöglicht das Organisieren von Studienmaterialien nach Fächern. Die **semantische Suche** basiert auf SentenceTransformers (all-MiniLM-L6-v2) und FAISS-Vektorindizes, die effizient die relevantesten Textpassagen finden. Die **Kontextbasierte Antwortgenerierung** nutzt das Mistral-Sprachmodell über Ollama, um natürlichsprachige Antworten zu formulieren, die sich strikt auf die Quelldokumente stützen. Besonders hervorzuheben ist die **Quellentransparenz**: Jede Antwort wird mit den verwendeten Dokumenten verlinkt, sodass Studierende die Informationen verifizieren können. Die **barrierefreie UI** implementiert einen indeterminierten Spinner für lange Wartezeiten, eine animierte Fortschrittsanzeige (Progressbar), Live-Regionen für Screenreader, vollständige Tastaturnavigation und eine Abbrechen-Funktion mit 5-Minuten-Timeout. Das System läuft komplett lokal, was Datenschutz und Offline-Verfügbarkeit garantiert.

## 6. Innovation

Die Innovation des Uni-Assistenten liegt in der **Kombination von RAG-Technologie mit strikter Barrierefreiheit**. Während viele AI-Lerntools entweder auf Cloud-APIs angewiesen sind oder Accessibility vernachlässigen, vereint dieser Assistent beides: lokale Ausführung für maximalen Datenschutz und WCAG 2.2 AA Konformität für inklusive Bildung. Die Implementierung eines **Warmup-Skripts**, das Machine-Learning-Modelle vor dem Flask-Start lädt, verhindert Timeouts und ermöglicht einen reibungslosen Betrieb auch in ressourcenbeschränkten Kubernetes-Umgebungen. Die **Fallback-Strategie** („Diese Frage kann ich nicht beantworten") minimiert Halluzinationen und stellt sicher, dass nur fundierte und Quellenbasierte Antworten gegeben werden. Der Einsatz von **indeterminierten Spinnern** in Kombination mit Progressbars und ARIA-Live-Regionen setzt neue Maßstäbe für die Nutzerfreundlichkeit von AI-Anwendungen mit langen Verarbeitungszeiten. Zudem ist der Uni-Assistent im Ganzen ein absolut neues nischen Produkt und kann einen neuen Markt erobern.

## 7. Wirkung (Impact)

Der Uni-Assistent hat das Potenzial, den Lernalltag von Studierenden nachhaltig zu verbessern. Durch die Möglichkeit, jederzeit spezifische Fragen zu Vorlesungsinhalten zu stellen, können Studierende **Verständnislücken sofort schließen**, anstatt auf Sprechstunden warten zu müssen. Die Quellenangaben fördern **wissenschaftliches Arbeiten** und ermutigen zur kritischen Überprüfung von Informationen. Besonders profitieren Studierende mit **Lernbehinderungen, ADHS oder Sehbehinderungen** von der barrierefreien Gestaltung: Screenreader-Nutzer erhalten semantisches Feedback über den Bearbeitungsfortschritt, und die klare Strukturierung mit ARIA-Attributen erleichtert die Navigation. Der **lokale Betrieb** schützt sensible Informationenvor unbefugtem Zugriff und eliminiert Abhängigkeiten von externen Diensten. Langfristig könnte der Uni-Assistent dazu beitragen, Bildung inklusiver und zugänglicher zu machen, indem er als Erweiterung für Learn-Management-Systeme wie Moodle dient.

## 8. Technische Exzellenz

Der Uni-Assistent nutzt ein modernes Tech-Stack: **Python 3.12** mit Flask als Web-Framework, **SentenceTransformers** (all-MiniLM-L6-v2) für die Generierung von 384-dimensionalen Embeddings, **FAISS** (Facebook AI Similarity Search) für effiziente Vektorsuche, und **Ollama** mit dem **Mistral-Modell** (4.4GB) für die Textgenerierung. Die Containerisierung erfolgt mit **Docker** (python:3.12-slim Base-Image), orchestriert durch **Kubernetes** mit zwei Services (uni-app, ollama) und separaten Deployments. **Security-Features** umfassen non-root User (UID 1001), dropped Linux Capabilities (ALL), no-new-privileges Flag, und read-only Root-Filesystems wo technisch möglich. Das **Warmup-Skript** lädt ML-Modelle proaktiv vor Flask-Start, und **Health-Checks** (Readiness/Liveness-Probes mit angepassten Timeouts) gewährleisten Stabilität. Die **Accessibility-Implementation** folgt WCAG 2.2 AA mit role="dialog", role="progressbar", aria-live="polite", Farbkontrast 7.3:1 (#005a9e auf #ffffff), und vollständigem Keyboard-Support.

## 9. Ethik, Transparenz und Inklusion

Der Uni-Assistent legt höchsten Wert auf **ethische AI-Nutzung**: Das System generiert keine Antworten ohne ausreichende Quellengrundlage und gibt explizit „Diese Frage kann ich nicht beantworten" zurück, wenn die Dokumente keine passenden Informationen enthalten. Diese **Anti-Halluzinations-Strategie** verhindert die Verbreitung von Fehlinformationen. Jede Antwort wird mit **Quellenangaben** transparent gemacht, sodass Studierende die Verlässlichkeit selbst überprüfen können. **Datenschutz** wird durch vollständig lokale Ausführung gewährleistet – keine Daten verlassen das System. Die **Inklusion** wird durch WCAG 2.2 AA Konformität sichergestellt: Screenreader-Kompatibilität, Tastaturnavigation, ausreichende Farbkontraste, alternative Texte, und semantisches HTML ermöglichen Menschen mit verschiedensten Behinderungen gleichberechtigten Zugang. Zudem werden momentan keine personenbezogenen Daten gespeichert oder analysiert.

## 10. Zukunftsvision

In 5–10 Jahren könnte der Uni-Assistent zu einer **universellen Lernplattform** weiterentwickelt werden, die nicht nur Fragen beantwortet, sondern auch **adaptive Lernpfade** erstellt. Durch Integration von **Spaced-Repetition-Algorithmen** könnte das System automatisch Wiederholungsfragen generieren und den Lernfortschritt tracken. **Multimodale Funktionen** wie Audio- und Video-Analyse würden es ermöglichen, auch Vorlesungsaufzeichnungen zu indexieren und durchsuchbar zu machen. Eine **kollaborative Komponente** könnte Studierenden erlauben, annotierte Notizen zu teilen und gemeinsam Wissensdatenbanken aufzubauen. Die **Integration mit Learning Management Systemen** (Moodle) würde den Workflow optimieren. **Fine-tuned Modelle** für spezifische Fachbereiche (Medizin, Jura, MINT) könnten die Antwortqualität weiter steigern. **Voice-Interfaces** und **AR-Brillen-Support** würden neue Interaktionsformen ermöglichen. Die Vision ist ein **inklusives, KI-gestütztes Bildungs-Ökosystem**, das lebenslanges Lernen für alle Menschen – unabhängig von Fähigkeiten, Herkunft oder finanziellen Mitteln – zugänglich und effektiv macht. Der Prototyp wurde für den gebrauch von Studierenden entwickelt, kann aber für Jede Art von Bildungseinrichtung optimiert werden wie z.B. Schulen oder Weiterbildungsanbietern. Zudem ist es Möglich das Grundgerüst für Unternehmen zu optimieren und aus der Hauptfunktion, dem Fragen stellen, die on-boarding Prozesse oder den Wissentransfer zu erleichtern. (vgl. Audio-Pitch)

---

## Technische Details

- **Sprache:** Python 3.12 — Python wurde für den Prototypen gewählt, weil es schnelle Entwicklung, eine große Auswahl an ML‑Bibliotheken (sentence-transformers, faiss) und eine niedrige Einstiegshürde bietet.
	- Warum so: Ermöglicht rasche Prototyp‑Iteration und einfache Integration von ML‑Tools.
	- Für Weiterentwicklung: Python für ML‑Logik beibehalten; I/O‑intensive Pfade asynchron (z. B. mit FastAPI) umsetzen.

- **Web‑Framework:** Flask (Prototyp)
	- Warum so: Sehr leichtgewichtig und schnell zu implementieren — ideal für Proof‑of‑Concept und UI‑getriebene Tests.
	- Für Skalierung: Wechsel zu FastAPI (ASGI, async, Pydantic‑Validation, automatische OpenAPI‑Docs) oder Betrieb hinter Gunicorn+UvicornWorker empfohlen.

- **AI‑Modell / Modellserver:** Mistral via Ollama (v0.3.12)
	- Warum so: Lokales Modellhosting über Ollama schützt Daten (keine externe Übertragung) und ist einfach integrierbar.
	- Hinweis: Modelle sind groß (mehrere GB). In Produktion: Persistente Volumes, InitContainer oder dedizierte Inference‑Services verwenden.

- **Embeddings:** SentenceTransformers (all‑MiniLM‑L6‑v2)
	- Warum so: Guter Kompromiss aus Genauigkeit, Geschwindigkeit und geringem Ressourcenbedarf (384‑dim).
	- Für Skalierung: Embeddings vorab berechnen, persistent speichern und inkrementell aktualisieren.

- **Vektorsuche:** FAISS (lokal)
	- Warum so: Schnelle, lokale ANN‑Suche mit direkter Kontrolle über Index und Storage.
	- Für Multi‑User/Produktiv: Managed oder verteilte Vektor‑DB (z. B. Milvus, Weaviate) für Skalierbarkeit, Replikation und einfache Backups.

- **Container:** Docker + Docker Compose (Entwicklung)
	- Warum so: Reproduzierbare lokale Entwicklung, einfache CI‑Pipeline.
	- Für Produktion: Multi‑stage Images, Dependency‑Pinning und Image‑Scanning in CI (Trivy).

- **Orchestrierung:** Kubernetes (2 Services: `uni-app`, `ollama`)
	- Warum so: Ermöglicht Skalierung, Rolling Updates, Health‑Checks und Ressourcenverwaltung.
	- Empfehlungen: App stateless gestalten, PersistentVolumes für Indizes/Modelle, separate Deployments für Inference‑Worker, HPA, NetworkPolicy, Ingress mit TLS.

- **Accessibility:** WCAG 2.2 AA konform
	- Warum so: Inklusion ist Kernziel — Screenreader, Tastaturnavigation, ARIA Live‑Regionen, ausreichender Farbkontrast und Fokus‑Management sind implementiert.
	- Weiterentwicklung: Nutzertests mit Screenreadern, automatisierte Accessibility‑Checks (z. B. axe‑core) in CI.

- **Architektur‑Empfehlungen für Mehrbenutzer‑Betrieb**
	- Statelesse Architektur: Sessions / Caches in Redis auslagern; keine Nutzerzustände lokal im Pod.
	- Asynchrone Verarbeitung: Längere Inferenzjobs über Queue (Celery/RQ) abarbeiten; API enqueued Job → Worker verarbeitet → Ergebnis in DB/Cache.
	- Modell‑Serving: Inference in dedizierten Worker‑Pods oder spezialisierten Model‑Servern (Triton, TorchServe, Ollama Cluster). Bei Bedarf auf kleinere Modelle oder GPU‑Nodes ausweichen.
	- Persistenz: Vektorindex und Embeddings auf PV/Blob speichern; regelmäßige Backups einplanen.
	- Observability & Ops: Prometheus + Grafana, zentrale Logs (Loki/ELK), Tracing (OpenTelemetry), und CI/CD (Build → Scan → Deploy).

---



---

**Autor:Aleksandar Deniz Veljkovic 
**Datum:** 15. November 2025  
**Kontakt: aleksandar.veljkovic@student.htw-berlin.de 