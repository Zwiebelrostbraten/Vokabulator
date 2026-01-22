import xml.etree.ElementTree as ET
import zipfile
from io import BytesIO
import os

x = 24755500
Name = "Lektions Name"
# Ihre Listen mit Fragen und Antworten
fragen = ["a/ab", "e/ex", "locus", "agnus", "animus", "arbor"]  # Fügen Sie hier Ihre Vokabeln hinzu
antworten = ["(mit Ablativ), Von, von..her", 1, "Ort", "Lamm", "Geist", "Baum"]  # Fügen Sie hier Ihre Übersetzungen hinzu

def save_by2(by2_filepath, Data):
    x = 24755500
    # Die Wurzel des XML-Dokuments erstellen
    root = ET.Element("BYXML", {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "version": "1.0",
        "xsi:noNamespaceSchemaLocation": "https://www.brainyoo.de/Brainyoo2/xsd/brainyoo_xml_v2.0.xsd"
    })
    Name = os.path.splitext(os.path.basename(by2_filepath))[0]
    # Eine Lektion hinzufügen
    lesson = ET.SubElement(root, "lesson", {
        "title": Name,
        "userLessonID": f"{x}"
    })
    x += 1
    #Data_scheme = {"Stilmittel": [list(Zeile eins), list(rest)]}  # Beispiel für Ihre Datenstruktur

    lessons = list(Data.keys())

    # Vokabelkarten für jede Frage und Antwort hinzufügen
    for lession in lessons:
        sublesson = ET.SubElement(lesson, "lesson", {
        "title": lession,
        "userLessonID": f"{x}"
        })
        x += 1
        fragen = Data[lession][0]
        antworten = Data[lession][1]
        for frage, antwort in zip(fragen, antworten):
            vocab_card = ET.SubElement(sublesson, "vocabularycard", {
                
                "userCardID": f"{x}"  # Hier sollten Sie eine eindeutige ID für jede Karte generieren
            })
            vocab_question = ET.SubElement(vocab_card, "vocabularyQuestion")
            vocab_para_q = ET.SubElement(vocab_question, "vocabPara")
            vocab_q = ET.SubElement(vocab_para_q, "vocabulary")
            vocab_q.text = str(frage)

            vocab_answer = ET.SubElement(vocab_card, "vocabularyAnswer")
            vocab_para_a = ET.SubElement(vocab_answer, "vocabPara")
            vocab_a = ET.SubElement(vocab_para_a, "vocabulary")
            vocab_a.text = str(antwort)

            x += 1
        x += 1    


    xml_data = BytesIO()
    tree = ET.ElementTree(root)
    tree.write(xml_data, encoding='utf-8', xml_declaration=True)

    xml_data.seek(0)
    print(by2_filepath)
    with zipfile.ZipFile(by2_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr('by_content.xml', xml_data.read())

