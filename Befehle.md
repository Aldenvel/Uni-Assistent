# Befehle für Uni-Assistent

## Kubernetes (Empfohlen für Projekt-Abgabe)

### Erste Schritte

```powershell
# 1. Alle Kubernetes-Ressourcen erstellen
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap-app.yaml
kubectl apply -f k8s/configmap-demo-docs.yaml
kubectl apply -f k8s/service-app.yaml
kubectl apply -f k8s/service-ollama.yaml
kubectl apply -f k8s/deployment-app.yaml
kubectl apply -f k8s/deployment-ollama.yaml

# 2. Warten bis Pods bereit sind
#    - Ollama InitContainer lädt automatisch Mistral (ca. 4-5 Minuten beim ersten Start)
#    - Danach starten beide Pods (ca. 30-60 Sekunden)
kubectl -n uni-assistent get pods -w

# 3. Port-Forward starten für Zugriff auf App
kubectl -n uni-assistent port-forward service/uni-app 5000:5000
```

App ist jetzt erreichbar unter: **http://localhost:5000**

---

### Status prüfen

```powershell
# Alle Pods anzeigen
kubectl -n uni-assistent get pods

# Pod-Details anzeigen
kubectl -n uni-assistent describe pod <pod-name>

# Logs anzeigen
kubectl -n uni-assistent logs -l app=uni-app --tail=50
kubectl -n uni-assistent logs -l app=ollama --tail=50

# Live-Logs verfolgen
kubectl -n uni-assistent logs -l app=uni-app -f

# Events anzeigen (für Fehlersuche)
kubectl -n uni-assistent get events --sort-by='.lastTimestamp'
```

---

### Nach Code-Änderungen

```powershell
# 1. Docker Image neu bauen
docker build -t uni-assistent-web:latest .

# 2. Deployment neu starten
kubectl -n uni-assistent rollout restart deployment/uni-app

# 3. Warten bis neuer Pod läuft
Start-Sleep -Seconds 30
kubectl -n uni-assistent get pods

# 4. Port-Forward neu starten
kubectl -n uni-assistent port-forward service/uni-app 5000:5000
```

---

### Stoppen

```powershell
# Port-Forward beenden
Stop-Process -Name kubectl -Force -ErrorAction SilentlyContinue

# Alle Ressourcen löschen
kubectl delete namespace uni-assistent
```

---

### Neustart der kompletten App

```powershell
# Deployments neu starten
kubectl -n uni-assistent rollout restart deployment/uni-app
kubectl -n uni-assistent rollout restart deployment/ollama

# Warten bis Pods laufen
Start-Sleep -Seconds 30
kubectl -n uni-assistent get pods

# Mistral-Modell prüfen (falls nötig neu laden)
kubectl -n uni-assistent exec deployment/ollama -- ollama list
kubectl -n uni-assistent exec deployment/ollama -- ollama pull mistral

# Port-Forward starten
kubectl -n uni-assistent port-forward service/uni-app 5000:5000
```

---

## Docker Compose (Alternative, einfacher)

### Starten

```powershell
# App im Hintergrund starten
docker-compose up -d

# Logs anzeigen
docker-compose logs -f

# Status prüfen
docker-compose ps
```

App ist erreichbar unter: **http://localhost:5000**

### Stoppen

```powershell
# Container stoppen
docker-compose down

# Container stoppen und Volumes löschen
docker-compose down -v
```

### Nach Code-Änderungen

```powershell
# Image neu bauen und Container neu starten
docker-compose up -d --build
```

---

## Häufige Probleme

### Port-Forward verliert Verbindung

```powershell
# Alle kubectl-Prozesse beenden
Stop-Process -Name kubectl -Force -ErrorAction SilentlyContinue

# Port-Forward neu starten
kubectl -n uni-assistent port-forward service/uni-app 5000:5000
```

### Pod crasht mit OOMKilled

```powershell
# Pod-Status prüfen
kubectl -n uni-assistent describe pod <pod-name> | Select-String -Pattern "OOM|memory"

# Ressourcen in deployment-app.yaml oder deployment-ollama.yaml erhöhen
# Dann Deployment neu starten:
kubectl apply -f k8s/deployment-app.yaml
kubectl -n uni-assistent rollout restart deployment/uni-app
```

### Mistral-Modell fehlt

```powershell
# Prüfen ob Modell geladen ist
kubectl -n uni-assistent exec deployment/ollama -- ollama list

# Modell neu laden
kubectl -n uni-assistent exec deployment/ollama -- ollama pull mistral
```

### "Failed to fetch" Fehler

1. Prüfen ob Port-Forward läuft: `Get-Process kubectl`
2. Prüfen ob Pod läuft: `kubectl -n uni-assistent get pods`
3. Logs prüfen: `kubectl -n uni-assistent logs -l app=uni-app --tail=50`
4. Port-Forward neu starten (siehe oben)

---

## Wichtige Dateien

- **k8s/**: Kubernetes-Konfigurationsdateien
- **docker-compose.yaml**: Docker Compose Konfiguration
- **dockerfile**: Docker Image Definition
- **app.py**: Flask-Hauptanwendung
- **core/**: RAG-Engine, Vektor-Suche, Ollama-Interface
- **templates/frage.html**: Accessible Loading UI (WCAG 2.2 AA)
- **Data/config.json**: App-Konfiguration
- **Uni/**: Ordner für eigene Dokumente (in Docker Compose gemountet)

---

## Ressourcen-Übersicht

### uni-app Pod
- CPU: 500m Request, 2 CPU Limit
- Memory: 1Gi Request, 2Gi Limit
- Enthält: Flask, SentenceTransformer (all-MiniLM-L6-v2), FAISS

### ollama Pod
- CPU: 2 CPU Request, 4 CPU Limit
- Memory: 12Gi Request, 32Gi Limit
- Modell: Mistral (4.4GB) - **wird automatisch beim Start geladen**
- InitContainer lädt Modell falls nicht vorhanden

### Warmup-Skript
- Lädt SentenceTransformer-Modell vor Flask-Start
- Verhindert Timeouts bei ersten Requests

### Health Checks
- Readiness: 30s initial delay, 10s period
- Liveness: 45s initial delay, 20s period, 3 failures erlaubt

---

## Accessibility Features (WCAG 2.2 AA)

Die App implementiert barrierefreie Loading-Indikatoren:

- **role="dialog"** mit aria-modal für Overlay
- **role="progressbar"** mit aria-valuenow/min/max
- **Indeterminate Spinner** mit role="status" und aria-live="polite"
- **sr-only Text** "Bitte warten …" für Screenreader
- **Fokus-Management**: Dialog → Antwort-Überschrift
- **Abbrechen-Button** mit AbortController
- **5-Minuten Timeout** für lange Mistral-Generierung
- **Farbkontrast**: #005a9e auf #ffffff (7.3:1)

---

## Demo-Daten

Der Ordner `Uni/Spezielle Programmierung/` enthält Demo-Dokumente:
- docker.txt
- kubernetes.txt
- vektordatenbanken.txt
- embeddings.txt
- rag.txt

Diese werden automatisch im initContainer der uni-app erstellt.

---

## Tipps

1. **Docker Desktop RAM**: Mindestens 16GB empfohlen für Mistral
2. **Kubernetes Context**: Sollte auf `docker-desktop` stehen
3. **Port 5000**: Muss frei sein (nicht von anderen Apps belegt)
4. **Geduld**: Mistral-Antworten können bis zu 5 Minuten dauern
5. **Logs**: Bei Problemen immer zuerst Logs prüfen





Perfekt! Die Pods werden jetzt gestoppt. Beim nächsten Start brauchst du nur:

```
# Deployments wieder auf 1 Replica hochfahren
kubectl -n uni-assistent scale deployment/uni-app --replicas=1
kubectl -n uni-assistent scale deployment/ollama --replicas=1

# Warten bis Pods laufen
Start-Sleep -Seconds 30
kubectl -n uni-assistent get pods

# Port-Forward starten
kubectl -n uni-assistent port-forward service/uni-app 5000:5000
```
Alle Konfigurationen bleiben erhalten:
✅ Namespace existiert weiter

✅ ConfigMaps bleiben

✅ Services bleiben

✅ Mistral-Modell muss **NICHT** neu geladen werden

✅ Alle YAML-Dateien unverändert

Die App ist jetzt komplett gestoppt und verbraucht keine Ressourcen mehr! 🎉