# Uni-Assistent – AI-gestützter Lernbegleiter

## 1. Executive Summary

Der Uni-Assistent ist ein intelligenter Lernbegleiter, der Studierenden hilft, ihre Vorlesungsmaterialien besser zu verstehen und effektiver zu lernen. Das System verwendet Retrieval-Augmented Generation (RAG) in Kombination mit einem lokalen Sprachmodell (Mistral via Ollama), um präzise Antworten auf Fragen zu Studieninhalten zu liefern. Die Anwendung läuft vollständig lokal in Docker-Containern und kann über Kubernetes orchestriert werden. Besonders hervorzuheben ist die barrierefreie Benutzeroberfläche nach WCAG 2.2 AA Standard, die allen Studierenden – unabhängig von individuellen Einschränkungen – gleichberechtigten Zugang ermöglichen soll. Das System analysiert hochgeladene Dokumente, erstellt einen Vektorindex und beantwortet dann spezifische Fragen unter Angabe der verwendeten Quellen.

## 2. Ziele des Projekts

Das Hauptziel des Uni-Assistenten ist es, die Lerneffizienz von Studierenden zu steigern und gleichzeitig Barrieren beim Zugang zu Bildungsinhalten abzubauen. Viele Studierende kämpfen mit der Menge an Vorlesungsmaterialien und haben Schwierigkeiten, relevante Informationen schnell zu finden oder komplexe Zusammenhänge zu verstehen. Der Uni-Assistent löst dieses Problem, indem er als intelligenter Ansprechpartner fungiert, der rund um die Uhr verfügbar ist und maßgeschneiderte Antworten auf individuelle Fragen liefert. Dabei werden ausschließlich die eigenen Studienmaterialien als Wissensquelle verwendet, was Halluzinationen minimiert und die Verlässlichkeit der Antworten maximiert. Ein weiteres wichtiges Ziel ist die Inklusion: Durch die Implementierung von WCAG 2.2 AA Accessibility-Features können auch Studierende mit Sehbehinderungen oder motorischen Einschränkungen das System vollständig nutzen.

## 3. Anwendung und Nutzung

Der Uni-Assistent richtet sich primär an Studierende aller Fachrichtungen, die ihre Lernmaterialien digital vorliegen haben. Die Nutzung erfolgt über eine webbasierte Oberfläche: Studierende hinterlegen den Pfad zu Ihren Vorlesungsskripten, PDFs oder Textdokumente hoch und organisieren diese nach Fächern. Anschließend können sie natürlichsprachige Fragen stellen wie „Was ist Docker?" oder „Erkläre den Unterschied zwischen Pods und Deployments in Kubernetes". Das System durchsucht die relevanten Dokumente semantisch, findet die passendsten Textpassagen und generiert eine fundierte Antwort unter Angabe der Quellen. Die barrierefreie Oberfläche mit Screenreader-Unterstützung, Tastaturnavigation und visuellen sowie akustischen Fortschrittsanzeigen ermöglicht auch Studierenden mit Behinderungen eine selbstständige Nutzung.

**Code-Repository:** [GitHub-Link hier einfügen]  
**Pitch:** [Audio-Link hier einfügen]

## 4. Entwicklungsstand

Das Projekt befindet sich im Status eines **funktionsfähigen Prototyps**. Alle Kernfunktionen sind implementiert und getestet: Die RAG-Pipeline funktioniert zuverlässig, die Vektorsuche liefert relevante Ergebnisse, und das Ollama-Modell generiert präzise Antworten basierend auf den Quelldokumenten. Die Docker-Containerisierung ist abgeschlossen, und die Kubernetes-Deployments mit zwei Services (uni-app und ollama) laufen stabil. Die barrierefreie Benutzeroberfläche wurde nach WCAG 2.2 AA Richtlinien implementiert und umfasst alle erforderlichen ARIA-Attribute, Fokus-Management und alternative Texte. Der Prototyp ist bereits einsatzbereit für den persönlichen Gebrauch und könnte mit weiteren Features wie Nutzerauthentifizierung, Cloud-Deployment und Multi-User-Support zur produktionsreifen Anwendung weiterentwickelt werden.

## 5. Projektdetails

Der Uni-Assistent bietet mehrere Kernfunktionen: **Dokumenten-Upload und -Verwaltung** ermöglicht das Organisieren von Studienmaterialien nach Fächern. Die **semantische Suche** basiert auf SentenceTransformers (all-MiniLM-L6-v2) und FAISS-Vektorindizes, die effizient die relevantesten Textpassagen finden. Die **Kontextbasierte Antwortgenerierung** nutzt das Mistral-Sprachmodell über Ollama, um natürlichsprachige Antworten zu formulieren, die sich strikt auf die Quelldokumente stützen. Besonders hervorzuheben ist die **Quellentransparenz**: Jede Antwort wird mit den verwendeten Dokumenten verlinkt, sodass Studierende die Informationen verifizieren können. Die **barrierefreie UI** implementiert einen indeterminierten Spinner für lange Wartezeiten, eine animierte Fortschrittsanzeige (Progressbar), Live-Regionen für Screenreader, vollständige Tastaturnavigation und eine Abbrechen-Funktion mit 5-Minuten-Timeout. Das System läuft komplett lokal, was Datenschutz und Offline-Verfügbarkeit garantiert.

## 6. Innovation

Die Innovation des Uni-Assistenten liegt in der **Kombination von RAG-Technologie mit strikter Barrierefreiheit**. Während viele AI-Lerntools entweder auf Cloud-APIs angewiesen sind oder Accessibility vernachlässigen, vereint dieser Assistent beides: lokale Ausführung für maximalen Datenschutz und WCAG 2.2 AA Konformität für inklusive Bildung. Die Implementierung eines **Warmup-Skripts**, das Machine-Learning-Modelle vor dem Flask-Start lädt, verhindert Timeouts und ermöglicht einen reibungslosen Betrieb auch in ressourcenbeschränkten Kubernetes-Umgebungen. Die **Fallback-Strategie** („Diese Frage kann ich nicht beantworten") minimiert Halluzinationen und stellt sicher, dass nur fundierte und Quellenbasierte Antworten gegeben werden. Der Einsatz von **indeterminierten Spinnern** in Kombination mit Progressbars und ARIA-Live-Regionen setzt neue Maßstäbe für die Nutzerfreundlichkeit von AI-Anwendungen mit langen Verarbeitungszeiten. Zudem ist der Uni-Assistent einer der wenigen RAG-Systeme, der vollständig in Kubernetes mit Security-Best-Practices (non-root user, read-only filesystems wo möglich) betrieben werden kann.

## 7. Wirkung (Impact)

Der Uni-Assistent hat das Potenzial, den Lernalltag von Studierenden nachhaltig zu verbessern. Durch die Möglichkeit, jederzeit spezifische Fragen zu Vorlesungsinhalten zu stellen, können Studierende **Verständnislücken sofort schließen**, anstatt auf Sprechstunden warten zu müssen. Die Quellenangaben fördern **wissenschaftliches Arbeiten** und ermutigen zur kritischen Überprüfung von Informationen. Besonders profitieren Studierende mit **Lernbehinderungen, ADHS oder Sehbehinderungen** von der barrierefreien Gestaltung: Screenreader-Nutzer erhalten akustisches Feedback über den Bearbeitungsfortschritt, und die klare Strukturierung mit ARIA-Attributen erleichtert die Navigation. Der **lokale Betrieb** schützt sensible Studienmaterialien vor unbefugtem Zugriff und eliminiert Abhängigkeiten von externen Diensten. Langfristig könnte der Uni-Assistent dazu beitragen, Bildung inklusiver und zugänglicher zu machen, indem er als Erweiterung für Learn-Management-Systeme wie Moodle dient..

## 8. Technische Exzellenz

Der Uni-Assistent nutzt ein modernes Tech-Stack: **Python 3.12** mit Flask als Web-Framework, **SentenceTransformers** (all-MiniLM-L6-v2) für die Generierung von 384-dimensionalen Embeddings, **FAISS** (Facebook AI Similarity Search) für effiziente Vektorsuche, und **Ollama** mit dem **Mistral-Modell** (4.4GB) für die Textgenerierung. Die Containerisierung erfolgt mit **Docker** (python:3.12-slim Base-Image), orchestriert durch **Kubernetes** mit zwei Services (uni-app, ollama) und separaten Deployments. **Security-Features** umfassen non-root User (UID 1001), dropped Linux Capabilities (ALL), no-new-privileges Flag, und read-only Root-Filesystems wo technisch möglich. Das **Warmup-Skript** lädt ML-Modelle proaktiv vor Flask-Start, und **Health-Checks** (Readiness/Liveness-Probes mit angepassten Timeouts) gewährleisten Stabilität. Die **Accessibility-Implementation** folgt WCAG 2.2 AA mit role="dialog", role="progressbar", aria-live="polite", Farbkontrast 7.3:1 (#005a9e auf #ffffff), und vollständigem Keyboard-Support.

## 9. Ethik, Transparenz und Inklusion

Der Uni-Assistent legt höchsten Wert auf **ethische AI-Nutzung**: Das System generiert keine Antworten ohne ausreichende Quellengrundlage und gibt explizit „Diese Frage kann ich nicht beantworten" zurück, wenn die Dokumente keine relevanten Informationen enthalten. Diese **Anti-Halluzinations-Strategie** verhindert die Verbreitung von Fehlinformationen. Jede Antwort wird mit **Quellenangaben** transparent gemacht, sodass Studierende die Verlässlichkeit selbst überprüfen können. **Datenschutz** wird durch vollständig lokale Ausführung gewährleistet – keine Daten verlassen das System. Die **Inklusion** wird durch WCAG 2.2 AA Konformität sichergestellt: Screenreader-Kompatibilität, Tastaturnavigation, ausreichende Farbkontraste, alternative Texte, und semantisches HTML ermöglichen Menschen mit verschiedensten Behinderungen gleichberechtigten Zugang. Zudem werden keine personenbezogenen Daten gespeichert oder analysiert.

## 10. Zukunftsvision

In 5–10 Jahren könnte der Uni-Assistent zu einer **universellen Lernplattform** weiterentwickelt werden, die nicht nur Fragen beantwortet, sondern auch **adaptive Lernpfade** erstellt. Durch Integration von **Spaced-Repetition-Algorithmen** könnte das System automatisch Wiederholungsfragen generieren und den Lernfortschritt tracken. **Multimodale Funktionen** wie Audio- und Video-Analyse würden es ermöglichen, auch Vorlesungsaufzeichnungen zu indexieren und durchsuchbar zu machen. Eine **kollaborative Komponente** könnte Studierenden erlauben, annotierte Notizen zu teilen und gemeinsam Wissensdatenbanken aufzubauen. Die **Integration mit Learning Management Systemen** (Moodle, Canvas) würde den Workflow optimieren. **Fine-tuned Modelle** für spezifische Fachbereiche (Medizin, Jura, MINT) könnten die Antwortqualität weiter steigern. **Voice-Interfaces** und **AR-Brillen-Support** würden neue Interaktionsformen ermöglichen. Die Vision ist ein **inklusives, KI-gestütztes Bildungs-Ökosystem**, das lebenslanges Lernen für alle Menschen – unabhängig von Fähigkeiten, Herkunft oder finanziellen Mitteln – zugänglich und effektiv macht.

---

## Technische Details

- **Sprache:** Python 3.12
- **Web-Framework:** Flask
- **AI-Modell:** Mistral (via Ollama 0.3.12)
- **Embeddings:** SentenceTransformers (all-MiniLM-L6-v2)
- **Vektorsuche:** FAISS
- **Container:** Docker + Docker Compose
- **Orchestrierung:** Kubernetes (2 Services: uni-app, ollama)
- **Accessibility:** WCAG 2.2 AA konform

---

**Autor:Aleksandar Deniz Veljkovic 
**Datum:** 15. November 2025  
**Kontakt: aleksandar.veljkovic@student.htw-berlin.de 