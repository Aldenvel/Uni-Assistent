#!/usr/bin/env python3
"""
Warmup-Skript: Lädt SentenceTransformer-Modelle vor Flask-Start.
Verhindert Timeouts bei ersten Health-Checks.
"""
import os
import sys

print("[WARMUP] Starte Modell-Preload...")

# SentenceTransformer-Modell laden (lädt ~80MB herunter/aus Cache)
try:
    from sentence_transformers import SentenceTransformer
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    print(f"[WARMUP] Lade SentenceTransformer-Modell: {model_name}")
    model = SentenceTransformer(model_name)
    
    # Test-Embedding generieren um sicherzustellen, dass alles geladen ist
    test_embedding = model.encode(["Test"], show_progress_bar=False)
    print(f"[WARMUP] Modell erfolgreich geladen. Embedding-Dimension: {len(test_embedding[0])}")
    
except Exception as e:
    print(f"[WARMUP] Fehler beim Laden des Modells: {e}", file=sys.stderr)
    sys.exit(1)

print("[WARMUP] Preload abgeschlossen. Flask-App kann jetzt starten.")
