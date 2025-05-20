import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def erzeuge_embedding(text):
    return EMBEDDING_MODEL.encode([text])[0]
#    # Erstelle den Cache-Ordner, falls er nicht existiert
def get_cache_pfade(fach):
    cache_ordner = os.path.join("data", "cache", fach)
    os.makedirs(cache_ordner, exist_ok=True)
    index_pfad = os.path.join(cache_ordner, "index.faiss")
    meta_pfad = os.path.join(cache_ordner, "metadaten.pkl")
    return index_pfad, meta_pfad

#    # Überprüfe, ob der Cache-Ordner existiert
def baue_index_und_texte(dokumente, fach="allgemein"):
    index_pfad, meta_pfad = get_cache_pfade(fach)
#    # Überprüfe, ob der Index und die Metadaten bereits existieren
    if os.path.exists(index_pfad) and os.path.exists(meta_pfad):
        index = faiss.read_index(index_pfad)
        with open(meta_pfad, "rb") as f:
            mapping = pickle.load(f)
        return index, mapping
#    # Wenn der Index nicht existiert, erstelle ihn neu
    texte = []
    mapping = []
    for doc in dokumente:
        absätze = [a.strip() for a in doc["text"].split("\n\n") if a.strip()]
        for absatz in absätze:
            texte.append(absatz)
            mapping.append({"text": absatz, "quelle": doc["quelle"]})

#    # Erstelle die Embeddings für alle Texte
    embeddings = [erzeuge_embedding(text) for text in texte]
    embeddings_np = np.array(embeddings).astype("float32")
#    # Erstelle den FAISS-Index
    index = faiss.IndexFlatL2(embeddings_np.shape[1])
    index.add(embeddings_np)
#    # Speichere den Index und die Metadaten
    with open(meta_pfad, "wb") as f:
        pickle.dump(mapping, f)
    faiss.write_index(index, index_pfad)

    return index, mapping
#    # Suche nach relevanten Texten
def finde_relevante_texte(frage, index, mapping, top_k=5):
    embedding = erzeuge_embedding(frage).astype("float32").reshape(1, -1)
    abstaende, ids = index.search(embedding, top_k)
#    # IDs der nächsten Nachbarn abrufen
    ergebnisse = []
    for idx in ids[0]:
        if idx < len(mapping):
            ergebnisse.append(mapping[idx])
    return ergebnisse
