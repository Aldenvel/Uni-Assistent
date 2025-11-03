import os
from core.document_loader import lade_dokumente_aus_ordner
from core.rag_engine import frage_beantworten
from core.ollama_interface import frage_an_modell_stellen
from core.quiz_engine import generiere_quizfrage
from core.quiz_engine import evaluiere_freitext_antwort  # Antwortauswertung importieren
from core.quiz_engine import starte_quiz_session  # Quiz-Session importieren
from core.config_manager import lade_benutzerpfad, speichere_benutzerpfad

def waehle_fach(basisordner):
    fächer = [f for f in os.listdir(basisordner) if os.path.isdir(os.path.join(basisordner, f))]

    if not fächer:
        print("Keine Fächer gefunden.")
        return None

    print("\nVerfügbare Fächer:")
    for i, fach in enumerate(fächer):
        print(f"[{i+1}] {fach}")

    eingabe = input("\nGib die Nummer oder den Namen des Fachs ein: ").strip()

    if eingabe.isdigit():
        index = int(eingabe) - 1
        if 0 <= index < len(fächer):
            return fächer[index]
    elif eingabe in fächer:
        return eingabe

    print("Ungültige Eingabe.")
    return None

def main():
    basisordner = lade_benutzerpfad()
    if not basisordner:
    print("Es wurde noch kein Basisordner konfiguriert.")
    eingabe = input("Bitte gib den Pfad zu deinem Uni-Ordner ein: ").strip()
    if os.path.isdir(eingabe):
        speichere_benutzerpfad(eingabe)
        basisordner = eingabe
        print("Pfad gespeichert.")
    else:
        print("Ungültiger Pfad.")
        return


    fach = waehle_fach(basisordner)
    if not fach:
        return

    pfad = os.path.join(basisordner, fach)
    texte = lade_dokumente_aus_ordner(pfad)

    if not texte:
        print("Keine lesbaren Dokumente gefunden.")
        return

    print(f"\n{len(texte)} Dokumente aus dem Fach '{fach}' geladen.")

    modus = input("\n(1) Frage stellen, (2) Quiz starten, (3) falsch wiederholen, (4) geplante Wiederholung starten > ").strip()

    if modus == "1":
        frage = input("\nWas möchtest du wissen? > ").strip()
        relevante_chunks = frage_beantworten(frage, texte)
        antwort = frage_beantworten(frage, texte, fach)
        print("\nAntwort:\n")
        print(antwort)

    elif modus == "2":
        runden = input("Wie viele Quizfragen möchtest du machen? (Standard: 5) > ").strip()
        anzahl = int(runden) if runden.isdigit() else 5
        starte_quiz_session(texte, fach, anzahl)
    elif modus == "3":
        from core.quiz_engine import starte_wiederholung
        starte_wiederholung(fach)
    elif modus == "4":
        from core.quiz_engine import starte_spaced_wiederholung
        starte_spaced_wiederholung(fach)
    else:
        print("Ungültige Auswahl.")

if __name__ == "__main__":
    main()
