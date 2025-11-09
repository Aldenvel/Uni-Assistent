# core/ollama_interface.py
import ollama
import re

STANDARD_KEINE_INFO = (
    "Diese Frage kann ich nicht beantworten, da hierzu keine Informationen in den Unterlagen zu finden waren."
)

# Stop-Token: Modell stoppt nach dem ersten Absatz
_DEF_STOP = ["\n\n"]

_NOT_FOUND_RE = re.compile(r"^\s*NOT_FOUND\s*$", re.IGNORECASE)


def _build_prompt(frage: str, kontext: str) -> str:
    """
    Baut den User-Prompt für Ollama.
    Der Prompt enthält ausschließlich die eigentliche Aufgabenstellung, den gegebenen Kontext
    und die Frage des Nutzers – ohne systemische Instruktionen oder Metaregeln.
    """
    return (
        "Beantworte die folgende Frage ausschließlich anhand der bereitgestellten AUSZÜGE.\n"
        "Wenn die Antwort nicht direkt in den AUSZÜGEN zu finden ist, antworte exakt mit 'NOT_FOUND'.\n\n"
        "AUSZÜGE:\n"
        f"{kontext}\n\n"
        f"FRAGE: {frage}\n\n"
        "ANTWORT:"
    )


def frage_an_modell_stellen(frage, kontext, modell_name: str = "mistral"):
    """
    Stellt eine Frage an das Ollama-Modell mit einem strikt kontextgebundenen Prompt.
    Aktuell werden die Antworten nicht mehr auf ein spezielles 'ANSWER:'-Format geprüft,
    sondern direkt zurückgegeben, solange das Modell nicht explizit 'NOT_FOUND' schreibt.
    """
    if not kontext or all(not k or not k.strip() for k in kontext):
        return STANDARD_KEINE_INFO

    context_text = "\n\n---\n\n".join(kontext).strip()
    if not context_text:
        return STANDARD_KEINE_INFO

    prompt = _build_prompt(frage, context_text)

    system_prompt = (
        "Du bist ein streng kontextgebundener Assistent. "
        "Du darfst ausschließlich Informationen aus den AUSZÜGEN verwenden. "
        "Wenn die Frage nicht eindeutig aus den AUSZÜGEN beantwortet werden kann, "
        "antworte exakt mit NOT_FOUND."
    )

    try:
        response = ollama.chat(
            model=modell_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            options={
                "temperature": 0,
                "top_p": 1,
                "top_k": 1,
                "num_predict": 256,
                "stop": _DEF_STOP,
            },
        )

        text = (response.get("message", {}) or {}).get("content", "") or ""
        text = text.strip()

        # Wenn das Modell explizit 'NOT_FOUND' schreibt → Standardantwort
        if _NOT_FOUND_RE.match(text):
            return STANDARD_KEINE_INFO

        # Ansonsten die Antwort direkt zurückgeben
        return text if text else STANDARD_KEINE_INFO

    except Exception as e:
        return f"Fehler bei der Modellabfrage: {e}"
