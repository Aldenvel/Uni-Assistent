import ollama

def frage_an_modell_stellen(frage, kontext, modell_name='mistral'):
    """
    Nutzt ein Ollama-Modell, um eine Antwort auf die Frage zu generieren,
    basierend auf den relevanten Kontexttexten.
    """
    prompt = "Hier ist ein Auszug aus meinen Unterlagen:\n\n"
    prompt += "\n\n".join(kontext)
    prompt += f"\n\nBeantworte bitte die folgende Frage dazu:\n{frage}"

    response = ollama.chat(
        model=modell_name,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response['message']['content']
