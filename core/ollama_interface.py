# core/ollama_interface.py
import ollama
import re

STANDARD_KEINE_INFO = (
    "Diese Frage kann ich nicht beantworten, da hierzu keine Informationen in den Unterlagen zu finden waren."
)

_DEF_STOP = ["\n\n"]

_ANSWER_RE = re.compile(r"^\s*ANSWER:\s*(.+)\s*$", re.IGNORECASE | re.DOTALL)
_NOT_FOUND_RE = re.compile(r"^\s*NOT_FOUND\s*$", re.IGNORECASE)

def _build_prompt(frage: str, kontext: str) -> str:
    return (
        "Aufgabe: Beantworte die Frage ausschließlich anhand der folgenden AUSZÜGE.\n"
        "Wenn die AUSZÜGE die Frage nicht beantworten, gib NUR 'NOT_FOUND' aus.\n"
        "Gib KEINE Erklärungen, KEINE Begründungen und KEINE Zusatzinformationen.\n\n"
        "Output-Formate (genau eines, exakt so):\n"
        "1) NOT_FOUND\n"
        "2) ANSWER: <eine kurze, präzise Antwort NUR basierend auf den AUSZÜGEN>\n\n"
        "AUSZÜGE:\n"
        f"{kontext}\n\n"
        f"FRAGE: {frage}\n\n"
        "ANTWORT:"
    )

def frage_an_modell_stellen(frage, kontext, modell_name="mistral"):
    if not kontext or all(not k or not k.strip() for k in kontext):
        return STANDARD_KEINE_INFO

    context_text = "\n\n---\n\n".join(kontext).strip()
    if not context_text:
        return STANDARD_KEINE_INFO

    prompt = _build_prompt(frage, context_text)

    try:
        resp = ollama.chat(
            model=modell_name,
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0.0,
                "top_p": 0.0,
                "top_k": 1,
                "num_predict": 256,
                "stop": _DEF_STOP,
            },
        )
        text = (resp.get("message", {}) or {}).get("content", "") or ""
        text = text.strip()

        if _NOT_FOUND_RE.match(text):
            return STANDARD_KEINE_INFO

        m = _ANSWER_RE.match(text)
        if m:
            answer = m.group(1).strip()
            return answer if answer else STANDARD_KEINE_INFO

        return STANDARD_KEINE_INFO

    except Exception as e:
        return f"Fehler bei der Modellabfrage: {e}"
