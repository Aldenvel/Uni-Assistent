from core.vektor_suche import baue_index_und_texte, finde_relevante_texte
# Diese Funktion beantwortet eine Frage, indem sie relevante Textstellen aus einem Dokumenten-Array abruft.
def frage_beantworten(frage, texte, fach):
    # Nutze FAISS-Index + Caching pro Fach
    index, mapping = baue_index_und_texte(texte, fach=fach)
#    # Frage in ein Embedding umwandeln
    # Relevante Textstellen finden
    relevante_chunks = finde_relevante_texte(frage, index, mapping)
#    # Extrahiere den Text aus den relevanten Textstellen
    return relevante_chunks
