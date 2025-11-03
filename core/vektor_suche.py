import os
import faiss
import pickle
import numpy as np
import hashlib
from sentence_transformers import SentenceTransformer

# === Embedding-Modell nur einmal laden ===
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def _hash_docs(dokumente):
    """Signatur über alle Dokumente, um Cache eindeutig zu machen."""
    h = hashlib.md5()
    for d in dokumente:
        h.update((d.get("quelle", "") + "\n" + d.get("text", "")).encode("utf-8", errors="ignore"))
    return h.hexdigest()

def get_cache_pfade(fach, sig):
    base = os.path.join("data", "cache", fach)
    os.makedirs(base, exist_ok=True)
    return (
        os.path.join(base, f"index_{sig}.faiss"),
        os.path.join(base, f"meta_{sig}.pkl"),
    )

def erzeuge_embeddings(texts):
    """Batched + normalisierte Embeddings (Cosine)."""
    if not texts:
        return np.zeros((0, 384), dtype="float32")
    embs = EMBEDDING_MODEL.encode(
        texts,
        batch_size=64,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True,  # already L2-normalized
    )
    return embs.astype("float32")

def baue_index_und_texte(dokumente, fach="allgemein"):
    """
    Erstellt/lädt FAISS-Index (Cosine via Inner Product) + Mapping.
    Cache basiert auf Inhalts-Hash, damit kein unnötiger Rebuild.
    """
    sig = _hash_docs(dokumente)
    index_pfad, meta_pfad = get_cache_pfade(fach, sig)

    if os.path.exists(index_pfad) and os.path.exists(meta_pfad):
        try:
            index = faiss.read_index(index_pfad)
            with open(meta_pfad, "rb") as f:
                mapping = pickle.load(f)
            return index, mapping
        except Exception:
            pass  # kaputter Cache -> Neuaufbau

    texte, mapping = [], []
    for doc in dokumente:
        absätze = [a.strip() for a in doc["text"].split("\n\n") if a.strip()]
        for absatz in absätze:
            texte.append(absatz)
            mapping.append({"text": absatz, "quelle": doc["quelle"]})

    if not texte:
        return faiss.IndexFlatIP(384), []

    embeddings = erzeuge_embeddings(texte)
    index = faiss.IndexFlatIP(embeddings.shape[1])  # Cosine via inner product
    index.add(embeddings)

    with open(meta_pfad, "wb") as f:
        pickle.dump(mapping, f)
    faiss.write_index(index, index_pfad)
    return index, mapping

def finde_relevante_texte(frage, index, mapping, top_k=5):
    """(Kompatibilität) – liefert nur Chunks ohne Scores."""
    if not mapping or index.ntotal == 0:
        return []
    q = erzeuge_embeddings([frage])
    D, I = index.search(q, top_k)
    ergebnisse = []
    for idx in I[0]:
        if 0 <= idx < len(mapping):
            ergebnisse.append(mapping[idx])
    return ergebnisse

def finde_relevante_texte_mit_scores(frage, index, mapping, top_k=5):
    """
    Liefert [(text, quelle, score)] – score ist Cosine-Ähnlichkeit [-1..1].
    Bei unserem Setup (normalized + IP) ist D direkt der Cosine-Score.
    """
    if not mapping or index.ntotal == 0:
        return []
    q = erzeuge_embeddings([frage])
    D, I = index.search(q, top_k)
    ergebnisse = []
    for score, idx in zip(D[0].tolist(), I[0].tolist()):
        if 0 <= idx < len(mapping):
            item = dict(mapping[idx])
            item["score"] = float(score)
            ergebnisse.append(item)
    return ergebnisse
