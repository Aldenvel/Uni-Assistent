#!/bin/sh
# check_and_pull_model.sh
# Prüft ob Mistral-Modell vorhanden ist und lädt es bei Bedarf herunter

echo "[INIT] Prüfe ob Mistral-Modell verfügbar ist..."

# Warte kurz, damit Ollama-Server bereit ist
sleep 5

# Prüfe ob Modell existiert
if ollama list | grep -q "mistral"; then
    echo "[INIT] Mistral-Modell ist bereits vorhanden."
else
    echo "[INIT] Mistral-Modell nicht gefunden. Starte Download..."
    ollama pull mistral
    echo "[INIT] Mistral-Modell erfolgreich heruntergeladen."
fi

echo "[INIT] Modell-Check abgeschlossen."
