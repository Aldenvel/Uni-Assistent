from core.ollama_interface import frage_an_modell_stellen
import random
import re
import os
import csv
from datetime import datetime
from datetime import timedelta
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Modell lokal für Quizfragen verwenden
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def texte_in_chunks_aufteilen(texte, chunk_size=500):
    chunks = []
    for eintrag in texte:
        inhalt = eintrag["text"]
        quelle = eintrag["quelle"]
        absätze = inhalt.split('\n\n')
        current = ""
        for absatz in absätze:
            if len(current) + len(absatz) < chunk_size:
                current += absatz + "\n\n"
            else:
                chunks.append({
                    "text": current.strip(),
                    "quelle": quelle
                })
                current = absatz + "\n\n"
        if current.strip():
            chunks.append({
                "text": current.strip(),
                "quelle": quelle
            })
    return chunks

def finde_relevante_chunks(frage, chunks, top_k=3):
    frage_vec = embedding_model.encode([frage])
    chunk_vecs = embedding_model.encode([c["text"] for c in chunks])
    ähnlichkeit = cosine_similarity(frage_vec, chunk_vecs)[0]
    top_indices = ähnlichkeit.argsort()[::-1][:top_k]
    relevante = [chunks[i] for i in top_indices]
    return relevante

def stelle_lernstand_datei_sicher(fach):
    ordner = "data/lernstand"
    os.makedirs(ordner, exist_ok=True)  # Falls der Ordner noch nicht existiert, anlegen

    pfad = os.path.join(ordner, f"{fach}.csv")
    if not os.path.exists(pfad):
        with open(pfad, "w", encoding="utf-8") as f:
            f.write("datum,fragetyp,frage,korrekt,benutzerantwort,musterantwort,anzahl_richtig_in_folge,naechste_wiederholung,letzter_status\n")
    return pfad

def berechne_naechste_wiederholung(anzahl_richtig):
    if anzahl_richtig < 5:
        return datetime.today()
    elif anzahl_richtig == 5:
        return datetime.today() + timedelta(days=3)
    elif anzahl_richtig == 6:
        return datetime.today() + timedelta(days=5)
    elif anzahl_richtig == 7:
        return datetime.today() + timedelta(days=7)
    else:
        return datetime.today() + timedelta(days=random.choice([5, 6, 7]))


def speichere_frage_und_antwort(fach, fragetyp, frage, korrekt, benutzerantwort, musterantwort):
    pfad = stelle_lernstand_datei_sicher(fach)
    zeilen = []
    existiert = False

    # Wenn die Datei schon Daten enthält, aktualisieren statt anhängen
    if os.path.exists(pfad):
        with open(pfad, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["frage"] == frage:
                    existiert = True
                    anzahl_richtig = int(row["anzahl_richtig_in_folge"])
                    if korrekt:
                        anzahl_richtig += 1
                    else:
                        anzahl_richtig = 0
                    row["anzahl_richtig_in_folge"] = str(anzahl_richtig)
                    row["naechste_wiederholung"] = berechne_naechste_wiederholung(anzahl_richtig).strftime("%Y-%m-%d")
                    row["letzter_status"] = str(int(korrekt))
                    row["benutzerantwort"] = benutzerantwort
                    row["musterantwort"] = musterantwort
                zeilen.append(row)

    if not existiert:
        zeilen.append({
            "datum": datetime.now().strftime("%Y-%m-%d"),
            "fragetyp": fragetyp,
            "frage": frage.replace("\n", " ").strip(),
            "korrekt": int(korrekt),
            "benutzerantwort": benutzerantwort.replace("\n", " ").strip(),
            "musterantwort": musterantwort.replace("\n", " ").strip(),
            "anzahl_richtig_in_folge": "1" if korrekt else "0",
            "naechste_wiederholung": berechne_naechste_wiederholung(1 if korrekt else 0).strftime("%Y-%m-%d"),
            "letzter_status": str(int(korrekt))
        })

    # Datei neu schreiben
    with open(pfad, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "datum", "fragetyp", "frage", "korrekt", "benutzerantwort", "musterantwort",
            "anzahl_richtig_in_folge", "naechste_wiederholung", "letzter_status"
        ])
        writer.writeheader()
        writer.writerows(zeilen)

FRAGETYPEN = ["wahr_falsch", "multiple_choice", "freitext"]

def generiere_quizfrage(texte, fach, modell_name='mistral'):
    chunks = texte_in_chunks_aufteilen(texte)
    simulierter_input = "Erstelle eine typische Prüfungsfrage zu diesem Fachbereich."
    relevante_chunks = finde_relevante_chunks(simulierter_input, chunks, top_k=3)

    typ = random.choice(FRAGETYPEN)

    prompt = f"""
Du bist ein intelligenter Lernassistent für das Fach "{fach}".
Basierend auf folgendem Dokumenteninhalt, stelle eine Prüfungsfrage vom Typ: {typ.upper()}.

KONTEXT:
{chr(10).join(chunk["text"] for chunk in relevante_chunks)}

FRAGE:
- Bei "wahr_falsch": Gib eine Aussage + Lösung (wahr oder falsch)
- Bei "multiple_choice": Gib Frage + A, B, C, D + richtige Antwort (z. B. "C")
- Bei "freitext": Stelle eine offene Frage + gib eine ideale Antwort mit 2–7 Schlüsselbegriffen
"""

    antwort = frage_an_modell_stellen("Erzeuge eine Lernfrage", [prompt], modell_name)

    # Quellen-Pfade extrahieren
    quellen = list({chunk["quelle"] for chunk in relevante_chunks})
    return typ, antwort, quellen


def evaluiere_freitext_antwort(user_antwort, modell_antwort):
    user_antwort = user_antwort.lower()
    muster = modell_antwort.lower()
    begriffe = set(re.findall(r'\b\w{5,}\b', muster))
    gefunden = [wort for wort in begriffe if wort in user_antwort]
    abdeckung = len(gefunden) / len(begriffe) if begriffe else 0
    korrekt = abdeckung >= 0.5
    return korrekt, list(gefunden), list(begriffe)


def evaluiere_wahr_falsch(user_input, modell_antwort):
    user_input = user_input.lower().strip()
    korrekt = "wahr" in modell_antwort.lower()
    if user_input in ["wahr", "w"]:
        return korrekt
    elif user_input in ["falsch", "f"]:
        return not korrekt
    return False


def evaluiere_multiple_choice(user_input, modell_antwort):
    user_input = user_input.strip().upper()
    match = re.search(r"richtige[r]? antwort[:]? ([A-D])", modell_antwort, re.IGNORECASE)
    if match:
        korrekt = match.group(1).upper()
        return user_input == korrekt
    return False


def starte_quiz_session(texte, fach, anzahl=5, modell_name='mistral'):
    punkte = 0

    for nummer in range(1, anzahl + 1):
        print(f"\nFrage {nummer} von {anzahl}")
        typ, quiz = generiere_quizfrage(texte, fach, modell_name)
        print(f"\nFragetyp: {typ.upper()}")
        print(quiz)

        user_input = input("\nDeine Antwort: ").strip()
        korrekt = False
        musterloesung = ""

        if typ == "freitext":
            teile = quiz.split("Antwort:")
            if len(teile) == 2:
                musterloesung = teile[1].strip()
                korrekt, gefunden, erwartet = evaluiere_freitext_antwort(user_input, musterloesung)

                if korrekt:
                    print("Richtig!")
                else:
                    print("Leider nicht korrekt.")
                    print(f"Erwartete Begriffe: {', '.join(erwartet)}")
                    print(f"Deine Begriffe: {', '.join(gefunden)}")
                    print("Musterlösung:")
                    print(musterloesung)
            else:
                print("Antwortformat nicht erkannt.")

        elif typ == "wahr_falsch":
            korrekt = evaluiere_wahr_falsch(user_input, quiz)
            print("Richtig!" if korrekt else "Leider nicht korrekt.")

        elif typ == "multiple_choice":
            korrekt = evaluiere_multiple_choice(user_input, quiz)
            print("Richtig!" if korrekt else "Leider nicht korrekt.")

        else:
            print("Fragetyp nicht unterstützt.")

        # Speicher nach jedem Fragetyp
        speichere_frage_und_antwort(
            fach=fach,
            fragetyp=typ,
            frage=quiz,
            korrekt=korrekt,
            benutzerantwort=user_input,
            musterantwort=musterloesung
        )

        if korrekt:
            punkte += 1

    print(f"\nQuiz beendet. Du hast {punkte} von {anzahl} Punkten erreicht.")
def starte_wiederholung(fach, modell_name="mistral"):
    pfad = stelle_lernstand_datei_sicher(fach)
    if not os.path.exists(pfad):
        print(f"Für das Fach '{fach}' wurden noch keine Lernstandsdaten gespeichert.")
        return

    falsch_beantwortet = []
    with open(pfad, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for zeile in reader:
            if zeile["korrekt"] == "0":
                falsch_beantwortet.append(zeile)

    if not falsch_beantwortet:
        print("Keine falsch beantworteten Fragen zum Wiederholen gefunden.")
        return

    print(f"\nWiederholung: {len(falsch_beantwortet)} Fragen aus dem Fach '{fach}'\n")
    punkte = 0

    for i, eintrag in enumerate(falsch_beantwortet, 1):
        print(f"\nFrage {i}:")
        print(eintrag["frage"])
        user_input = input("Deine Antwort: ").strip()
        korrekt = False

        if eintrag["fragetyp"] == "freitext":
            musterloesung = eintrag["musterantwort"]
            korrekt, gefunden, erwartet = evaluiere_freitext_antwort(user_input, musterloesung)
            if korrekt:
                print("Richtig!")
            else:
                print("Leider nicht korrekt.")
                print(f"Erwartete Begriffe: {', '.join(erwartet)}")
                print(f"Deine Begriffe: {', '.join(gefunden)}")
                print("Musterlösung:")
                print(musterloesung)

        elif eintrag["fragetyp"] == "wahr_falsch":
            korrekt = evaluiere_wahr_falsch(user_input, eintrag["frage"])
            print("Richtig!" if korrekt else "Leider nicht korrekt.")

        elif eintrag["fragetyp"] == "multiple_choice":
            korrekt = evaluiere_multiple_choice(user_input, eintrag["frage"])
            print("Richtig!" if korrekt else "Leider nicht korrekt.")

        if korrekt:
            punkte += 1

    print(f"\nWiederholung abgeschlossen. Richtig beantwortet: {punkte} von {len(falsch_beantwortet)}")
def starte_spaced_wiederholung(fach):
    pfad = stelle_lernstand_datei_sicher(fach)
    heute = datetime.today().date()

    if not os.path.exists(pfad):
        print(f"Für das Fach '{fach}' wurden noch keine Lernstandsdaten gespeichert.")
        return

    faellige_fragen = []
    with open(pfad, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                wiederholungstag = datetime.strptime(row["naechste_wiederholung"], "%Y-%m-%d").date()
                if wiederholungstag <= heute:
                    faellige_fragen.append(row)
            except:
                continue  # Falls Datum fehlt oder falsch formatiert ist

    if not faellige_fragen:
        print("Heute sind keine Fragen zur Wiederholung fällig.")
        return

    print(f"\nWiederholung: {len(faellige_fragen)} fällige Fragen aus dem Fach '{fach}'\n")
    punkte = 0

    for i, eintrag in enumerate(faellige_fragen, 1):
        print(f"\nFrage {i}:")
        print(eintrag["frage"])
        user_input = input("Deine Antwort: ").strip()
        korrekt = False

        if eintrag["fragetyp"] == "freitext":
            musterloesung = eintrag["musterantwort"]
            korrekt, gefunden, erwartet = evaluiere_freitext_antwort(user_input, musterloesung)
            if korrekt:
                print("Richtig!")
            else:
                print("Leider nicht korrekt.")
                print(f"Erwartete Begriffe: {', '.join(erwartet)}")
                print(f"Deine Begriffe: {', '.join(gefunden)}")
                print("Musterlösung:")
                print(musterloesung)

        elif eintrag["fragetyp"] == "wahr_falsch":
            korrekt = evaluiere_wahr_falsch(user_input, eintrag["frage"])
            print("Richtig!" if korrekt else "Leider nicht korrekt.")

        elif eintrag["fragetyp"] == "multiple_choice":
            korrekt = evaluiere_multiple_choice(user_input, eintrag["frage"])
            print("Richtig!" if korrekt else "Leider nicht korrekt.")

        # Speichern (aktualisieren) mit neuem Status
        speichere_frage_und_antwort(
            fach=fach,
            fragetyp=eintrag["fragetyp"],
            frage=eintrag["frage"],
            korrekt=korrekt,
            benutzerantwort=user_input,
            musterantwort=eintrag["musterantwort"]
        )

        if korrekt:
            punkte += 1

    print(f"\nWiederholung abgeschlossen. Richtig beantwortet: {punkte} von {len(faellige_fragen)}")
