# Hilfe-Doku (Einsteigerfreundlich)



## 1. Überblick
Diese Anwendung ist ein Lern-Assistent. Er kann:
- Deine lokalen Uni-Dokumente einlesen
- Fragen dazu beantworten (nutzt RAG: sucht relevante Textstellen und fragt dann ein Sprachmodell)
- Quiz-Fragen generieren und deinen Lernfortschritt speichern
- Eine Zusammenfassung der Inhalte erstellen (API-Endpunkt)

Du kannst die App im Browser nutzen (HTML-Oberfläche) oder über API-Endpunkte (für Kubernetes / technische Tests).

## 2. Was wurde neu hinzugefügt / geändert
| Bereich | Änderung | Warum |
|--------|----------|-------|
| Sicherheit | Dockerfile gehärtet (kein root, kleines Basisimage) | Weniger Angriffsfläche |
| Volumes | `/app/Uni` nur lesend, `/app/data` schreibbar | Schutz Originaldaten vs. Lernstand + Cache |
| Healthcheck | Route `/healthz` + Healthcheck in docker-compose | Orchestrierung / Monitoring |
| API | `/api/frage/<fach>` und `/api/zusammenfassung/<fach>` | Erfüllt Kubernetes-Anforderung "nur API" |
| Kubernetes | Ordner `k8s/` mit Deployments & Services | Vorbereitung für kind-Cluster |
| Caching | RAG nutzt FAISS + Cache unter `data/cache` | Schnellere wiederholte Abfragen |
| Konsistenz | Standardantwort bei fehlendem Kontext | Verlässlichkeit statt Halluzination |

## 3. Wichtige Ordner & Dateien
| Pfad | Zweck |
|------|------|
| `app.py` | Flask Hauptanwendung (Routen + API) |
| `core/` | Logik: RAG (`rag_engine.py`), Vektorsuche (`vektor_suche.py`), Quizfunktionen |
| `data/` | Wird vom Container beschrieben: Konfiguration, Lernstand, Cache |
| `templates/` | HTML-Seiten für Browser-Oberfläche |
| `docker-compose.yaml` | Startet App + Ollama (Modellserver) lokal |
| `dockerfile` | Bauanleitung für Container-Image |
| `k8s/` | Kubernetes Ressourcen (Namespace, Deployments, Services) |
| `Hilfe-Doku.md` | Dieses Dokument |

## 4. Voraussetzungen
- Installiertes Docker Desktop (Windows)
- Optional: `kind` für lokales Kubernetes (falls du K8s testen möchtest)

## 5. Start (Docker) – Schritt für Schritt
1. Öffne PowerShell im Projektordner.
2. Baue die Container neu:
   ```powershell
   docker compose build --no-cache
   ```
3. Starte die Container:
   ```powershell
   docker compose up -d
   ```
4. Öffne deinen Browser: `http://localhost:5000`
5. Beim ersten Mal wirst du zur Einrichtung weitergeleitet. Gib ein: `/app/Uni` (das ist der Pfad IM Container)
6. Du siehst jetzt die Liste deiner Fächer (Ordner im Uni-Verzeichnis). Klicke eins an.
7. Optionen: Quiz, Wiederholung, Eigene Frage stellen.

## 6. API verwenden
Beispiel: Frage stellen zu Fach "Spezielle Programmierung".
```powershell
Invoke-RestMethod -Uri http://localhost:5000/api/frage/Spezielle%20Programmierung -Method POST -Body (@{frage='Was ist eine Funktion?'} | ConvertTo-Json) -ContentType 'application/json'
```
Antwort-Format:
```json
{
  "answer": "..." ,
  "fallback": false
}
```
Wenn kein Kontext gefunden wurde:
```json
{
  "answer": null,
  "fallback": true
}
```
Zusammenfassung:
```powershell
Invoke-RestMethod -Uri http://localhost:5000/api/zusammenfassung/Spezielle%20Programmierung -Method POST -Body '{}' -ContentType 'application/json'
```

## 7. Kubernetes Test (optional)
Vereinfachte Schritte (nur nötig, wenn du K8s zeigen willst):
```powershell
kind create cluster --name uni
# Image lokal bauen
docker build -t uni-assistent-web:latest .
# In kind laden
kind load docker-image uni-assistent-web:latest --name uni
# Ressourcen anwenden
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap-app.yaml
kubectl apply -f k8s/configmap-demo-docs.yaml
kubectl apply -f k8s/deployment-ollama.yaml
kubectl apply -f k8s/service-ollama.yaml
kubectl apply -f k8s/deployment-app.yaml
kubectl apply -f k8s/service-app.yaml
# Warte auf Pods (Ollama InitContainer lädt automatisch Mistral - ca. 5 Min)
kubectl -n uni-assistent get pods -w
# Port weiterleiten, damit du im Browser testen kannst
kubectl -n uni-assistent port-forward deploy/uni-app 5000:5000

```
Dann Browser: `http://localhost:5000/healthz` oder API testen.

## 8. Typische Probleme & Lösungen
| Problem | Ursache | Lösung |
|---------|---------|--------|
| Keine Fächer sichtbar | Falscher Pfad bei Setup | `/app/Uni` eingeben |
| Antwort leer / fallback | Kein relevanter Kontext gefunden | Prüfe Dokumente im Uni-Ordner |
| Container startet nicht | Docker nicht aktiv | Docker Desktop öffnen |
| Langsamer Start | Embedding-Modelle laden | 1–2 Minuten normal beim ersten Start |
| K8s Pod CrashLoop | Image nicht geladen im kind | `kind load docker-image ...` erneut ausführen |

## 9. Sicherheit (Kurz)
- Container läuft als normaler Benutzer (nicht root).
- Nur notwendige Schreibpfade (`/app/data`).
- Dokumente sind read-only.
- Healthcheck erleichtert Überwachung.
- Capabilities entfernt → weniger Rechte.

## 10. Was du noch machen musst
| Aufgabe | Status |
|---------|--------|
| Optional Fallback vereinheitlichen zu "Ich weiß es nicht" überall | Offen |
| Pitch (Audio 1–3 Min) aufnehmen | Offen |
| README final mit 10 Fragen schreiben | Offen |
| Kubernetes optional demonstrieren | Optional |

## 11. Nächste optionale Verbesserungen
- Audit-Log für jede KI-Anfrage
- Rate-Limiting (Schutz vor Spam)
- Mehr AI-Funktionen (z.B. Keyword-Extraktion)

## 12. Kurzer Technischer Überblick
- RAG: Zerlegt Dokumente, baut Vektorindex (FAISS), findet relevante Textstücke.
- Validierung: Wenn keine starken Treffer → Standardantwort statt Halluzination.
- Ollama: Lokaler Modell-Server (Mistral) für Antworten.
- Quiz: Speichert Lernstand in CSV (einfach portabel).

## 13. Kontakt / Hilfe
Wenn etwas nicht funktioniert: 
1. Logs ansehen:
   ```powershell
   docker compose logs web --tail 50
   docker compose logs ollama --tail 50
   ```
2. Prüfen ob Dokumente im Host-Pfad wirklich vorhanden sind.
3. API mit einer sehr einfachen Frage testen.

