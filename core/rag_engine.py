# core/rag_engine.py
import re
from typing import List, Tuple, List as TList
from core.vektor_suche import (
    baue_index_und_texte,
    finde_relevante_texte_mit_scores,
)
from core.ollama_interface import frage_an_modell_stellen

STANDARD_KEINE_INFO = (
    "Diese Frage kann ich nicht beantworten, da hierzu keine Informationen in den Unterlagen zu finden waren."
)

# sehr kleine Stopwortliste (de+en) – bewusst knapp gehalten
_STOP = {
    "der","die","das","und","oder","ein","eine","einer","einem","eines","mit","ohne","zu","zum","zur",
    "von","im","in","am","an","auf","für","ist","sind","war","waren","wird","werden","also","auch",
    "the","a","an","and","or","of","to","in","on","for","is","are","was","were","be","been","being"
}

def _tokens(s: str) -> TList[str]:
    return [t for t in re.split(r"[^a-zA-ZäöüÄÖÜß0-9]+", (s or "").lower()) if t and t not in _STOP]

def _content_tokens(s: str, min_len: int = 5) -> TList[str]:
    return [t for t in _tokens(s) if len(t) >= min_len]

def _token_overlap(a: str, b: str) -> Tuple[int, set]:
    ta, tb = set(_tokens(a)), set(_tokens(b))
    inter = ta & tb
    return len(inter), inter

def _filter_kontext(kandidaten, frage, min_sim_hart=0.45, min_sim_weich=0.25, min_overlap=1, top_k_final=5):
    """
    Harte Vorselektion (entschärfte Version):
    - Top1 >= min_sim_hart -> akzeptieren
    - sonst: Top1 >= min_sim_weich UND token-overlap >= min_overlap
    Danach bis zu top_k_final Chunks, die dieselbe Logik erfüllen.
    """
    if not kandidaten:
        return [], []

    top1 = kandidaten[0]
    top1_ok = (top1["score"] >= min_sim_hart)
    if not top1_ok:
        ovl_count, _ = _token_overlap(frage, top1["text"])
        top1_ok = (top1["score"] >= min_sim_weich and ovl_count >= min_overlap)
    if not top1_ok:
        return [], []

    kontext, quellen = [], []
    for item in kandidaten[:top_k_final]:
        if item["score"] >= min_sim_hart:
            kontext.append(item["text"])
            quellen.append(item["quelle"])
        else:
            ovl_count, _ = _token_overlap(frage, item["text"])
            if item["score"] >= min_sim_weich and ovl_count >= min_overlap:
                kontext.append(item["text"])
                quellen.append(item["quelle"])

    if not kontext:
        return [], []
    quellen = list(dict.fromkeys(quellen))
    return kontext, quellen

def _validate_answer_against_context(answer: str, kontext: TList[str],
                                     max_out_of_context_ratio: float = 0.6,
                                     min_required_hits: int = 1) -> bool:
    """
    Strikte Nachvalidierung (derzeit ungenutzt – kann später wieder aktiviert werden).
    """
    if not answer or not kontext:
        return False

    ans_tokens = _content_tokens(answer)
    if not ans_tokens:
        return False

    ctx_tokens = set()
    for c in kontext:
        ctx_tokens.update(_content_tokens(c))

    hits = [t for t in ans_tokens if t in ctx_tokens]
    misses = [t for t in ans_tokens if t not in ctx_tokens]

    if len(misses) / max(1, len(ans_tokens)) > max_out_of_context_ratio:
        return False

    if len(hits) < min_required_hits:
        return False

    return True

def frage_beantworten(frage, dokumente, fach, modell_name="mistral", top_k=8):
    """
    Vollständige RAG-Pipeline (ohne strikte Nachvalidierung):
    1) Semantisches Ranking (FAISS)
    2) Harte Vorselektion (Score + Overlap) -> kein Kontext -> Standardtext
    3) Modellantwort -> direkt zurückgeben, wenn vorhanden
    """
    index, mapping = baue_index_und_texte(dokumente, fach=fach)
    kandidaten = finde_relevante_texte_mit_scores(frage, index, mapping, top_k=top_k)
    print(f"[DEBUG] Gefundene Kandidaten: {len(kandidaten)}")

    if kandidaten:
        print(f"[DEBUG] Top-Score: {kandidaten[0]['score']:.3f} – Quelle: {kandidaten[0]['quelle']}")

    kontext, _ = _filter_kontext(kandidaten, frage)
    print(f"[DEBUG] Kontext gefunden: {len(kontext)} Textabschnitte")

    if not kontext:
        print("[DEBUG] Kein Kontext gefunden – gebe Standardantwort zurück.")
        return STANDARD_KEINE_INFO

    answer = frage_an_modell_stellen(frage, kontext, modell_name=modell_name)
    print(f"[DEBUG] Modellantwort (erste 200 Zeichen): {answer[:200]}")

    if not answer or not answer.strip():
        print("[DEBUG] Leere Antwort vom Modell – gebe Standardantwort zurück.")
        return STANDARD_KEINE_INFO

    print("[DEBUG] Antwort ohne Nachvalidierung zurückgegeben.")
    return answer

def frage_beantworten_mit_quellen(frage, dokumente, fach, modell_name="mistral", top_k=8):
    """
    Wie oben, zusätzlich: Quellenliste zurückgeben.
    """
    index, mapping = baue_index_und_texte(dokumente, fach=fach)
    kandidaten = finde_relevante_texte_mit_scores(frage, index, mapping, top_k=top_k)
    print(f"[DEBUG] [mit_quellen] Gefundene Kandidaten: {len(kandidaten)}")

    if kandidaten:
        print(f"[DEBUG] [mit_quellen] Top-Score: {kandidaten[0]['score']:.3f} – Quelle: {kandidaten[0]['quelle']}")

    kontext, quellen = _filter_kontext(kandidaten, frage)
    print(f"[DEBUG] [mit_quellen] Kontext gefunden: {len(kontext)} Textabschnitte")

    if not kontext:
        print("[DEBUG] [mit_quellen] Kein Kontext gefunden – gebe Standardantwort zurück.")
        return STANDARD_KEINE_INFO, []

    answer = frage_an_modell_stellen(frage, kontext, modell_name=modell_name)
    print(f"[DEBUG] [mit_quellen] Modellantwort (erste 200 Zeichen): {answer[:200]}")

    if not answer or not answer.strip():
        print("[DEBUG] [mit_quellen] Leere Antwort vom Modell – gebe Standardantwort zurück.")
        return STANDARD_KEINE_INFO, []

    print("[DEBUG] [mit_quellen] Antwort ohne Nachvalidierung zurückgegeben.")
    return answer, quellen
