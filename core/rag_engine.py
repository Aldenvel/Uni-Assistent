from core.vektor_suche import baue_index_und_texte, finde_relevante_texte

def frage_beantworten(frage, texte):
    """
    Erzeugt einen FAISS-Index aus den gegebenen Texten
    und liefert die relevantesten Abschnitte zur gestellten Frage zurück.
    """
    if not texte:
        return []

    index, mapping = baue_index_und_texte(texte)
    relevante_chunks = finde_relevante_texte(frage, index, mapping)

    return relevante_chunks
