# Uni-Assistent – Ki-gestützter Lernbegleiter

## 1. Executive Summary

Der Uni-Assistent ist ein intelligenter Lernbegleiter, der Studierenden hilft, ihre Vorlesungsmaterialien besser zu verstehen und effektiver zu lernen. Das System verwendet Retrieval-Augmented Generation (RAG) in Kombination mit einem lokalen Sprachmodell (Mistral via Ollama), um präzise Antworten auf Fragen zu Studieninhalten zu liefern. Die Anwendung läuft vollständig lokal in Docker-Containern und kann über Kubernetes orchestriert werden. Besonders hervorzuheben ist die barrierefreie Benutzeroberfläche nach WCAG 2.2 AA Standard, die allen Studierenden – unabhängig von individuellen Einschränkungen – gleichberechtigten Zugang ermöglichen soll. Das System analysiert hochgeladene Dokumente, erstellt einen Vektorindex und beantwortet dann spezifische Fragen unter Angabe der verwendeten Quellen. Zudem enthält der Uni-Assistent die Möglichkeit selbst oder mit Hilfe der KI Karteikarten zur Prüfungsvorbereitung zu erstellen, dabei gibt es verschiedene Stile (Multiple-Coice, Freitext, Wahr-/Falsch-Aussagen). Die Quize/Karteikarten sind mit einem Punktesystem implementiert, bei dem der reiz des lernens durch Wiederholung spielerisch behandelt wird.

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

Die Innovation des Uni-Assistenten liegt in der **Kombination von RAG-Technologie mit strikter Barrierefreiheit**. Während viele KI-Lerntools entweder auf Cloud-APIs angewiesen sind oder Accessibility vernachlässigen, abgesehen dass es keine Dokumentenbasierte Lern-Ki-Anwendung gibt,, vereint dieser Assistent beides: lokale Ausführung für maximalen Datenschutz und WCAG 2.2 AA Konformität für inklusive Bildung. Die Implementierung eines **Warmup-Skripts**, das Machine-Learning-Modelle vor dem Flask-Start lädt, verhindert Timeouts und ermöglicht einen reibungslosen Betrieb auch in ressourcenbeschränkten Kubernetes-Umgebungen. Die **Fallback-Strategie** („Diese Frage kann ich nicht beantworten") minimiert Halluzinationen und stellt sicher, dass nur fundierte und Quellenbasierte Antworten gegeben werden. Der Einsatz von **indeterminierten Spinnern** in Kombination mit Progressbars und ARIA-Live-Regionen setzt neue Maßstäbe für die Nutzerfreundlichkeit von KI-Anwendungen mit langen Verarbeitungszeiten. Zudem ist der Uni-Assistent im Ganzen ein absolut neues nischen Produkt und kann einen neuen Markt erobern.

## 7. Wirkung (Impact)

Der Uni-Assistent hat das Potenzial, den Lernalltag von Studierenden nachhaltig zu verbessern. Durch die Möglichkeit, jederzeit spezifische Fragen zu Vorlesungsinhalten zu stellen, können Studierende **Verständnislücken sofort schließen**, anstatt auf Sprechstunden warten zu müssen. Die Quellenangaben fördern **wissenschaftliches Arbeiten** und ermutigen zur kritischen Überprüfung von Informationen. Besonders profitieren Studierende mit **Lernbehinderungen, ADHS oder Sehbehinderungen** von der barrierefreien Gestaltung: Screenreader-Nutzer erhalten semantisches Feedback über den Bearbeitungsfortschritt, und die klare Strukturierung mit ARIA-Attributen erleichtert die Navigation. Der **lokale Betrieb** schützt sensible Informationenvor unbefugtem Zugriff und eliminiert Abhängigkeiten von externen Diensten. Langfristig könnte der Uni-Assistent dazu beitragen, Bildung inklusiver und zugänglicher zu machen, indem er als Erweiterung für Learn-Management-Systeme wie Moodle dient.

## 8. Technische Exzellenz

Der Uni-Assistent für den Prototypenein : **Python 3.12** mit Flask als Web-Framework, **SentenceTransformers** (all-MiniLM-L6-v2) für die Generierung von 384-dimensionalen Embeddings, **FAISS** (Facebook AI Similarity Search) für effiziente Vektorsuche, und **Ollama** mit dem **Mistral-Modell** (4.4GB) für die Textgenerierung. Die Containerisierung erfolgt mit **Docker** (python:3.12-slim Base-Image), orchestriert durch **Kubernetes** mit zwei Services (uni-app, ollama) und separaten Deployments. **Security-Features** umfassen non-root User (UID 1001), dropped Linux Capabilities (ALL), no-new-privileges Flag, und read-only Root-Filesystems wo technisch möglich. Das **Warmup-Skript** lädt ML-Modelle proaktiv vor Flask-Start, und **Health-Checks** (Readiness/Liveness-Probes mit angepassten Timeouts) gewährleisten Stabilität. Die **Accessibility-Implementation** folgt WCAG 2.2 AA mit role="dialog", role="progressbar", aria-live="polite", Farbkontrast 7.3:1 (#005a9e auf #ffffff), und vollständigem Keyboard-Support.

Entschieden habe ich mich für Python wegen dem Funktionsumfang und der einfachen und schnellen Entwicklung. Flask habe ich verwendet, weil es es für meinen Prototypen die beste Wahl war, für die Weiterentwicklung würde ich auf etwas stabilereres und sichereres umsteigen wie z.B. FastAPI. Für Mistral als KI-Modell habe ich mich entschieden, weil bei meinen recherchen zur damaligen Zeit, Mistral als ein lokales und europäisches Modell beworben wurde. Außerdem hatte ich gelesen, dass es es optimal im Wissenschaftlichen Kontext läuft, also Perfekt für den Uni-Assistenten. 

## 9. Ethik, Transparenz und Inklusion

Der Uni-Assistent legt höchsten Wert auf **ethische AI-Nutzung**: Das System generiert keine Antworten ohne ausreichende Quellengrundlage und gibt explizit „Diese Frage kann ich nicht beantworten" zurück, wenn die Dokumente keine passenden Informationen enthalten. Diese **Anti-Halluzinations-Strategie** verhindert die Verbreitung von Fehlinformationen. Jede Antwort wird mit **Quellenangaben** transparent gemacht, sodass Studierende die Verlässlichkeit selbst überprüfen können. **Datenschutz** wird durch vollständig lokale Ausführung gewährleistet – keine Daten verlassen das System. Die **Inklusion** wird durch WCAG 2.2 AA Konformität sichergestellt: Screenreader-Kompatibilität, Tastaturnavigation, ausreichende Farbkontraste, alternative Texte, und semantisches HTML ermöglichen Menschen mit verschiedensten Behinderungen gleichberechtigten Zugang. Zudem werden momentan keine personenbezogenen Daten gespeichert oder analysiert.

## 10. Zukunftsvision

In 5–10 Jahren könnte der Uni-Assistent zu einer **universellen Lernplattform** weiterentwickelt werden, die nicht nur Fragen beantwortet, sondern auch **adaptive Lernpfade** erstellt. Durch Integration von **Spaced-Repetition-Algorithmen** könnte das System automatisch Wiederholungsfragen generieren und den Lernfortschritt tracken. **Multimodale Funktionen** wie Audio- und Video-Analyse würden es ermöglichen, auch Vorlesungsaufzeichnungen zu indexieren und durchsuchbar zu machen. Eine **kollaborative Komponente** könnte Studierenden erlauben, annotierte Notizen zu teilen und gemeinsam Wissensdatenbanken aufzubauen. Die **Integration mit Learning Management Systemen** (Moodle) würde den Workflow optimieren. **Fine-tuned Modelle** für spezifische Fachbereiche (Medizin, Jura, MINT) könnten die Antwortqualität weiter steigern. **Voice-Interfaces** und **AR/VR-Brillen-Support** würden neue Interaktionsformen ermöglichen z.B. eine Frage aus der Physik mit einem Visuellen KI-Modell, dass Albert Einstein immitiert (Visuel und Auditiv), der dann den Studierenden Sprechstunden innerhalb des Ökösystems anbietet.. Die Vision ist ein **inklusives, KI-gestütztes Bildungs-Ökosystem**, das lebenslanges Lernen für alle Menschen – unabhängig von Fähigkeiten – zugänglich und effektiv macht. Der Prototyp wurde für den gebrauch von Studierenden entwickelt, kann aber für Jede Art von Bildungseinrichtung optimiert werden wie z.B. Schulen oder Weiterbildungsanbietern. Zudem ist es Möglich das Grundgerüst für Unternehmen zu optimieren und aus der Hauptfunktion, dem Fragen stellen, die on-boarding Prozesse oder den Wissentransfer zu erleichtern. (vgl. Audio-Pitch)

---

## Technische Details

- **Sprache:** Python 3.12 — Python wurde für den Prototypen gewählt, weil es schnelle Entwicklung, eine große Auswahl an ML‑Bibliotheken (sentence-transformers, faiss) und eine niedrige Einstiegshürde bietet.
	- Warum so: Ermöglicht rasche Prototyp‑Iteration und einfache Integration von ML‑Tools.
	- Für Weiterentwicklung: Python für ML‑Logik beibehalten; I/O‑intensive Pfade asynchron (z. B. mit FastAPI) umsetzen.

- **Web‑Framework:** Flask (Prototyp)
	- Warum so: Sehr leichtgewichtig und schnell zu implementieren — ideal für Proof‑of‑Concept und UI‑getriebene Tests.
	- Für Skalierung: Wechsel zu FastAPI (ASGI, async, Pydantic‑Validation, automatische OpenAPI‑Docs) oder Betrieb hinter Gunicorn+UvicornWorker empfohlen.

- **KI‑Modell / Modellserver:** Mistral via Ollama (v0.3.12)
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
	- Weiterentwicklung: automatisierte Accessibility‑Checks (z. B. axe‑core) in CI.

- **Architektur‑Empfehlungen für Mehrbenutzer‑Betrieb**
	- Statelesse Architektur: Sessions / Caches in Redis auslagern; keine Nutzerzustände lokal im Pod.
	- Asynchrone Verarbeitung: Längere Inferenzjobs über Queue (Celery/RQ) abarbeiten; API enqueued Job Worker verarbeitet > Ergebnis in DB/Cache.
	- Modell‑Serving: Inference in dedizierten Worker‑Pods oder spezialisierten Model‑Servern (Triton, TorchServe, Ollama Cluster). Bei Bedarf auf kleinere Modelle oder GPU‑Nodes ausweichen.
	- Persistenz: Vektorindex und Embeddings auf PV/Blob speichern; regelmäßige Backups einplanen.
	- Observability & Ops: Prometheus + Grafana, zentrale Logs (Loki/ELK), Tracing (OpenTelemetry), und CI/CD (Build > Scan > Deploy).

---



---

**Autor:Aleksandar Deniz Veljkovic (Aldenvel) 
**Datum:** 15. November 2025  
**Kontakt: aleksandar.veljkovic@student.htw-berlin.

Pitch als Text:
Hallo, wir sind AldenvelSolutions.
Wir möchten Ihnen heute einen KI-Lernassistenten vorstellen, der Studierenden, Schülern und Mitarbeitenden das Lernen einfacher, klarer und deutlich zugänglicher macht – ganz ohne Datenschutzrisiken und vollständig barrierefrei.

Studierende und Mitarbeitende verbringen unglaublich viel Zeit damit, Informationen in PDFs, Foliensätzen oder Skripten zu suchen.
Dazu kommen allgemeine KI-Systeme wie ChatGPT. Aber diese Systeme kennen die hinterlegten Unterlagen nicht. Sie mischen Internetwissen mit eigenen Vermutungen und liefern dadurch oft ungenaue oder falsche Antworten.

Unser Ansatz geht genau auf dieses Problem ein.

Wir haben einen KI-Lernassistenten entwickelt, der sich ausschließlich auf die offiziell hinterlegten Unterlagen einer Bildungseinrichtung oder eines Unternehmens konzentriert – und damit genau das liefert, was wirklich gebraucht wird.

Der Assistent umfasst drei wichtige Funktionen:

Erstens: Er beantwortet Fragen direkt aus den bereitgestellten Dokumenten.
Mit klar formulierten Antworten und eindeutigen Quellenangaben.
So weiß jeder sofort, woher die Information stammt.

Zweitens: Er erstellt automatisch Karteikarten und Quizfragen aus dem vorhandenen Material.
Das macht das Lernen leichter und hilft beim Wiederholen vor Prüfungen oder wichtigen Schulungen.

Drittens: Ein spielerisches Lern-Erfolgssystem sorgt für zusätzliche Motivation.
Nutzer sehen ihren Fortschritt, erhalten kleine Belohnungen und bleiben motivierter am Ball.
So fühlt sich Lernen deutlich angenehmer und strukturierter an.


Technisch arbeitet unser System lokal oder in einer kontrollierten Umgebung.
Alle Daten bleiben geschützt – und unter voller Kontrolle der Institution.
Die Antworten bleiben verlässlich, verständlich und frei von unnötigem Fremd-Wissen.

Unser aktueller Stand ist ein funktionierender Prototyp im Universitätsbereich mit sehr zufriedenen Test-Nutzern. Er nutzt echte Kursunterlagen, erstellt Lernmaterialien und beantwortet Fragen zuverlässig.

Jetzt möchten wir daraus eine vollständige Plattform entwickeln.
Eine Plattform, die Universitäten, Weiterbildungsanbietern und Unternehmen hilft, ihren eigenen maßgeschneiderten Lernassistenten zu implementieren.

Für Universitäten bedeutet das:
Ein persönlicher Lernbegleiter für jedes Fach.
Optional mit anonymisierten Auswertungen, die zeigen, wo Lernschwachstellen bestehen.  
Zudem gibt es die Möglichkeit der Integration in bestehende Lernsysteme wie zum Beispiel moodle. 


Für Unternehmen bedeutet das: ein verlässlicher Assistent für Onboarding, Wissenstransfer und Weiterbildung –
besonders in komplexen oder regulierten Bereichen, in denen sensible und vertrauliche Daten verarbeitet werden. 

Dafür suchen wir eine Finanzierungsbeteiligung in Höhe von 350.000 Euro um in den nächsten 9 Monaten aus dem Prototyp eine skalierbare Plattform zu schaffen, Schnittstellen zu entwickeln und Projekte mit Partnern aus Hochschulen und Unternehmen zu starten.

Wenn Sie früh in eine Lösung investieren möchten, die Lernen schneller, klarer und sicherer macht,
freuen wir uns auf das Gespräch mit Ihnen.

