import os
import json

CONFIG_DATEI = "data/config.json"

def lade_benutzerpfad():
    if not os.path.exists(CONFIG_DATEI):
        return None
    with open(CONFIG_DATEI, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("basisordner")

def speichere_benutzerpfad(pfad):
    os.makedirs("data", exist_ok=True)
    with open(CONFIG_DATEI, "w", encoding="utf-8") as f:
        json.dump({"basisordner": pfad}, f, ensure_ascii=False, indent=2)
