import os
import fitz  
import docx
from pptx import Presentation
from bs4 import BeautifulSoup
from ebooklib import epub

def extract_text_from_pdf(pfad):
    texte = []
    try:
        doc = fitz.open(pfad)
        for seite in doc:
            text = seite.get_text()
            if text:
                texte.append(text)
    except Exception as e:
        print(f"Fehler beim Lesen von PDF: {pfad} – {e}")
    return "\n".join(texte)

def extract_text_from_docx(pfad):
    doc = docx.Document(pfad)
    return "\n".join(para.text for para in doc.paragraphs if para.text.strip())

def extract_text_from_pptx(pfad):
    prs = Presentation(pfad)
    texte = []
    for folie in prs.slides:
        for shape in folie.shapes:
            if hasattr(shape, "text"):
                text = shape.text.strip()
                if text:
                    texte.append(text)
    return "\n".join(texte)

def extract_text_from_html(pfad):
    with open(pfad, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")
    return soup.get_text()

def extract_text_from_epub(pfad):
    book = epub.read_epub(pfad)
    texte = []
    for item in book.get_items():
        if item.get_type() == epub.EpubHtml:
            soup = BeautifulSoup(item.get_content(), "lxml")
            texte.append(soup.get_text())
    return "\n".join(texte)

def lade_dokumente_aus_ordner(ordnerpfad):
    texte = []
    for wurzel, _, dateien in os.walk(ordnerpfad):
        for datei in dateien:
            pfad = os.path.join(wurzel, datei)
            try:
                if datei.endswith(".pdf"):
                    text = extract_text_from_pdf(pfad)
                elif datei.endswith(".docx"):
                    text = extract_text_from_docx(pfad)
                elif datei.endswith(".pptx"):
                    text = extract_text_from_pptx(pfad)
                elif datei.endswith((".html", ".htm")):
                    text = extract_text_from_html(pfad)
                elif datei.endswith(".epub"):
                    text = extract_text_from_epub(pfad)
                else:
                    continue
                texte.append({"text": text, "quelle": pfad})
            except Exception as e:
                print(f"Fehler beim Laden von {pfad}: {e}")
    return texte
