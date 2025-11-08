# core/ollama_interface.py
import ollama
import re

STANDARD_KEINE_INFO = (
    "Diese Frage kann ich nicht beantworten, da hierzu keine Informationen in den Unterlagen zu finden waren."
)

# Stop-Token: Modell stoppt nach dem ersten Absatz
_DEF_STOP = ["\n\n"]

# Erlaubte Antwortformate
_ANSWER_RE = re.compile(r"^\s*ANSWER:\s*(.+)\s*$", re.IGNORECASE | re.DOTALL)
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


def frage_an_modell_stellen(frage, kontext, modell_name="mistral"):
    """
    Stellt eine Frage an das Ollama-Modell mit einem strikt kontrollierten Prompt.
    Das Modell darf nur auf Basis des Kontexts antworten.
    """
    if not kontext or all(not k or not k.strip() for k in kontext):
        return STANDARD_KEINE_INFO

    context_text = "\n\n---\n\n".join(kontext).strip()
    if not context_text:
        return STANDARD_KEINE_INFO

    prompt = _build_prompt(frage, context_text)

    system_prompt = (
        "SYSTEMANWEISUNG (verpflichtend): "
        "Du bist ein streng kontextgebundenes Analysemodell. "
        "Du darfst ausschließlich Informationen aus dem gegebenen Kontext ('AUSZÜGE') verwenden. "
        "Wenn die gestellte Frage nicht eindeutig durch diese Informationen beantwortet werden kann, "
        "musst du exakt mit 'NOT_FOUND' antworten. "
        "Du darfst KEINE eigenen Schlussfolgerungen, Vermutungen oder externes Wissen einbringen. "
        "Du darfst KEINEN Versuch unternehmen, die Antwort zu erraten oder zu ergänzen. "
        "Du darfst KEINE allgemeinen Informationen, Interpretationen oder Erklärungen hinzufügen. "
        "Wenn du unsicher bist oder keine exakte Antwort aus den AUSZÜGEN ableiten kannst, "
        "antworte mit 'NOT_FOUND'. "
    )

    try:
        response = ollama.chat(
            model=modell_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            options={
                "temperature": 0, # kann auch auf 0 gesetzt erden
                "top_p": 1, # kann auf 1 gesetzt werden 
                "top_k": 1,
                "num_predict": 256,
                "stop": _DEF_STOP,
            },
        )

        text = (response.get("message", {}) or {}).get("content", "") or ""
        text = text.strip()

        if _NOT_FOUND_RE.match(text):
            return STANDARD_KEINE_INFO

        match = _ANSWER_RE.match(text)
        if match:
            answer = match.group(1).strip()
            return answer if answer else STANDARD_KEINE_INFO

        return STANDARD_KEINE_INFO

    except Exception as e:
        return f"Fehler bei der Modellabfrage: {e}"
