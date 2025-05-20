from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import csv
from datetime import datetime
from core.config_manager import lade_benutzerpfad, speichere_benutzerpfad
from core.rag_engine import frage_beantworten
from core.ollama_interface import frage_an_modell_stellen
from core.document_loader import lade_dokumente_aus_ordner
from core.quiz_engine import (
    generiere_quizfrage,
    evaluiere_freitext_antwort,
    evaluiere_wahr_falsch,
    evaluiere_multiple_choice,
    speichere_frage_und_antwort,
    stelle_lernstand_datei_sicher
)

app = Flask(__name__)
app.config["BASIS_ORDNER"] = lade_benutzerpfad()

# Weiterleitung zur Einrichtung, falls kein Ordner gewählt wurde
@app.before_request
def weiterleitung_wenn_keine_einstellung():
    if not app.config["BASIS_ORDNER"] and request.endpoint not in ("setup", "waehle_ordner", "static"):
        return redirect(url_for("setup"))

@app.route("/setup", methods=["GET", "POST"])
def setup():
    if request.method == "POST":
        ordner = request.form["ordner"]
        if os.path.isdir(ordner):
            speichere_benutzerpfad(ordner)
            app.config["BASIS_ORDNER"] = ordner
            return redirect(url_for("index"))  # ← Benutzer wird zur Startseite geleitet
        else:
            return render_template("setup.html", fehler="Pfad ungültig.")
    return render_template("setup.html")

@app.route("/waehle_ordner")
def waehle_ordner():
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        pfad = filedialog.askdirectory(title="Ordner auswählen")
        return jsonify({"pfad": pfad if pfad else None})
    except Exception as e:
        return jsonify({"fehler": str(e)})

@app.route("/einstellungen", methods=["GET", "POST"])
def einstellungen():
    aktueller_pfad = app.config["BASIS_ORDNER"]
    erfolg = False

    if request.method == "POST":
        neuer_pfad = request.form.get("neuer_pfad")
        if neuer_pfad and os.path.isdir(neuer_pfad):
            speichere_benutzerpfad(neuer_pfad)
            app.config["BASIS_ORDNER"] = neuer_pfad
            aktueller_pfad = neuer_pfad
            erfolg = True

    return render_template("einstellungen.html", aktueller_pfad=aktueller_pfad, erfolg=erfolg)

# Fach-Menü: Auswahl Quiz / Wiederholung / Eigene Frage
@app.route("/fach/<fach>")
def fach_menue(fach):
    return render_template("fach_menue.html", fach=fach)

# Quiz-Modus: neue Frage oder Bewertung
@app.route("/quiz/<fach>", methods=["GET", "POST"])
def quiz(fach):
    pfad = os.path.join(app.config["BASIS_ORDNER"], fach)

    texte = lade_dokumente_aus_ordner(pfad)

    if request.method == "POST":
        user_input = request.form["antwort"]
        frage = request.form["frage"]
        typ = request.form["typ"]
        muster = request.form["muster"]

        korrekt = False
        feedback = ""
        gefunden = []
        erwartet = []

        if typ == "freitext":
            korrekt, gefunden, erwartet = evaluiere_freitext_antwort(user_input, muster)
            feedback = "Richtig!" if korrekt else "Leider nicht korrekt."
        elif typ == "wahr_falsch":
            korrekt = evaluiere_wahr_falsch(user_input, frage)
            feedback = "Richtig!" if korrekt else "Leider nicht korrekt."
        elif typ == "multiple_choice":
            korrekt = evaluiere_multiple_choice(user_input, frage)
            feedback = "Richtig!" if korrekt else "Leider nicht korrekt."

        speichere_frage_und_antwort(
            fach=fach,
            fragetyp=typ,
            frage=frage,
            korrekt=korrekt,
            benutzerantwort=user_input,
            musterantwort=muster
        )

        return render_template("quiz.html", frage=frage, fach=fach, antwort=user_input,
                               korrekt=korrekt, feedback=feedback, muster=muster,
                               gefunden=gefunden, erwartet=erwartet, beantwortet=True)

    # GET: neue Frage
    typ, frage, quellen  = generiere_quizfrage(texte, fach)
    musterloesung = ""
    if typ == "freitext" and "Antwort:" in frage:
        teile = frage.split("Antwort:")
        frage = teile[0].strip()
        musterloesung = teile[1].strip()

    return render_template("quiz.html", frage=frage, fach=fach, typ=typ,
                       muster=musterloesung, beantwortet=False, quellen=quellen)


# Spaced-Wiederholung: fällige Fragen wiederholen
@app.route("/wiederholung/<fach>", methods=["GET", "POST"])
def wiederholung(fach):
    pfad = os.path.join(app.config["BASIS_ORDNER"], fach)
    heute = datetime.today().date()

    fragen = []
    try:
        with open(stelle_lernstand_datei_sicher(fach), encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    datum = datetime.strptime(row["naechste_wiederholung"], "%Y-%m-%d").date()
                    if datum <= heute:
                        fragen.append(row)
                except:
                    continue
    except FileNotFoundError:
        fragen = []

    if not fragen:
        return render_template("wiederholung.html", fach=fach, abgeschlossen=True)

    if request.method == "POST":
        frage = request.form["frage"]
        typ = request.form["typ"]
        muster = request.form["muster"]
        antwort = request.form["antwort"]

        korrekt = False
        feedback = ""

        if typ == "freitext":
            korrekt, gefunden, erwartet = evaluiere_freitext_antwort(antwort, muster)
            feedback = "Richtig!" if korrekt else "Leider nicht korrekt."
        elif typ == "wahr_falsch":
            korrekt = evaluiere_wahr_falsch(antwort, frage)
            feedback = "Richtig!" if korrekt else "Leider nicht korrekt."
        elif typ == "multiple_choice":
            korrekt = evaluiere_multiple_choice(antwort, frage)
            feedback = "Richtig!" if korrekt else "Leider nicht korrekt."

        speichere_frage_und_antwort(
            fach=fach,
            fragetyp=typ,
            frage=frage,
            korrekt=korrekt,
            benutzerantwort=antwort,
            musterantwort=muster
        )

        return render_template("wiederholung.html", fach=fach, beantwortet=True,
                               frage=frage, antwort=antwort, korrekt=korrekt,
                               feedback=feedback, muster=muster)

    frage = fragen[0]
    return render_template("wiederholung.html", fach=fach, frage=frage["frage"],
                           typ=frage["fragetyp"], muster=frage["musterantwort"],
                        beantwortet=False)

# Eigene Frage an KI stellen
@app.route("/frage/<fach>", methods=["GET", "POST"])
def frage_stellen(fach):
    pfad = os.path.join(app.config["BASIS_ORDNER"], fach)
    texte = lade_dokumente_aus_ordner(pfad)

    antwort = None
    quellen = []

    if request.method == "POST":
        frage = request.form["frage"]
        relevante_chunks = frage_beantworten(frage, texte)

        if not relevante_chunks:
            antwort = "Es konnten keine passenden Informationen in deinen Dokumenten gefunden werden."
            quellen = []
        else:
            kontexttexte = [chunk["text"] for chunk in relevante_chunks]
            antwort = frage_an_modell_stellen(frage, kontexttexte)
            quellen = list({chunk["quelle"] for chunk in relevante_chunks})

    return render_template("frage.html", fach=fach, antwort=antwort, quellen=quellen)

@app.route("/editor/<fach>", methods=["GET", "POST"])
def editor(fach):
    if request.method == "POST":
        typ = request.form["fragetyp"]

        if typ == "freitext":
            frage = request.form["frage"]
            muster = request.form["muster"]

        elif typ == "wahr_falsch":
            frage = request.form["frage"]
            muster = request.form["muster"].lower()

        elif typ == "multiple_choice":
            frage = request.form["frage"]
            a = request.form["A"]
            b = request.form["B"]
            c = request.form["C"]
            d = request.form["D"]
            richtig = request.form["richtig"]
            muster = f"A. {a}\nB. {b}\nC. {c}\nD. {d}\nrichtige Antwort: {richtig}"

        else:
            return "Ungültiger Fragetyp", 400

        speichere_frage_und_antwort(
            fach=fach,
            fragetyp=typ,
            frage=frage,
            korrekt=False,
            benutzerantwort="",
            musterantwort=muster
        )

    # CSV einlesen und Fragenliste vorbereiten
    pfad = stelle_lernstand_datei_sicher(fach)
    fragen_liste = []

    try:
        with open(pfad, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for index, row in enumerate(reader):
                fragen_liste.append({
                    "id": index,
                    "frage": row["frage"],
                    "muster": row["musterantwort"],
                    "typ": row["fragetyp"]
                })
    except FileNotFoundError:
        pass

    return render_template("editor.html", fach=fach, erfolg=(request.method == "POST"), fragen=fragen_liste)
@app.route("/editor/<fach>/loeschen/<int:id>", methods=["POST"])

# Route zum Löschen einer Frage
def loesche_frage(fach, id):
    pfad = stelle_lernstand_datei_sicher(fach)

    fragen = []
    try:
        with open(pfad, encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            if 0 <= id < len(reader):
                del reader[id]  # Entferne die Zeile
                fragen = reader
    except FileNotFoundError:
        return "Datei nicht gefunden", 404

    # Neue Datei ohne die gelöschte Zeile schreiben
    with open(pfad, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "datum", "fragetyp", "frage", "korrekt",
            "benutzerantwort", "musterantwort",
            "anzahl_richtig_in_folge", "naechste_wiederholung", "letzter_status"
        ])
        writer.writeheader()
        writer.writerows(fragen)

    return redirect(f"/editor/{fach}")


@app.route("/editor/<fach>/bearbeiten/<int:id>", methods=["GET", "POST"])
def bearbeiten_frage(fach, id):
    pfad = stelle_lernstand_datei_sicher(fach)

    # CSV laden
    with open(pfad, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    if id >= len(reader):
        return "Frage nicht gefunden", 404

    if request.method == "POST":
        typ = request.form["fragetyp"]
        frage = request.form["frage"]
        muster = ""

        if typ == "freitext":
            muster = request.form["muster"]
        elif typ == "wahr_falsch":
            muster = request.form["muster"].lower()
        elif typ == "multiple_choice":
            a = request.form["A"]
            b = request.form["B"]
            c = request.form["C"]
            d = request.form["D"]
            richtig = request.form["richtig"]
            muster = f"A. {a}\nB. {b}\nC. {c}\nD. {d}\nrichtige Antwort: {richtig}"
        else:
            return "Ungültiger Fragetyp", 400

        # Aktualisieren
        reader[id]["frage"] = frage
        reader[id]["fragetyp"] = typ
        reader[id]["musterantwort"] = muster

        # Zurücksetzen des Lernstatus
        reader[id]["korrekt"] = "0"
        reader[id]["benutzerantwort"] = ""
        reader[id]["anzahl_richtig_in_folge"] = "0"
        reader[id]["naechste_wiederholung"] = datetime.today().strftime("%Y-%m-%d")
        reader[id]["letzter_status"] = "0"

        # Neu schreiben
        with open(pfad, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=reader[0].keys())
            writer.writeheader()
            writer.writerows(reader)
        return redirect(f"/editor/{fach}")

    # GET: vorausgefülltes Formular
    daten = reader[id]
    return render_template("bearbeiten.html", fach=fach, id=id, eintrag=daten)
# Route für die Startseite
@app.route("/")
def index():
    basis_ordner = app.config["BASIS_ORDNER"]
    fächer = []
    if basis_ordner and os.path.isdir(basis_ordner):
        fächer = [f for f in os.listdir(basis_ordner) if os.path.isdir(os.path.join(basis_ordner, f))]
    return render_template("index.html", fächer=fächer)

# App starten
if __name__ == "__main__":
    app.run(debug=True, port=5000) 
