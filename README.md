# 📚 Vokabulator

> Ein kleines Windows-Programm, mit dem man aus lateinischen Texten automatisch Vokabellisten erstellt.

---

## Beschreibung

**Vokabulator** liest einen lateinischen Text ein, fragt alle enthaltenen Wörter automatisch bei [Navigium](https://www.navigium.de) ab und generiert daraus eine strukturierte Vokabelliste. Die Liste kann als Excel-Datei oder als Brainyoo-Kartei (`.by2`) exportiert werden – ideal für Schüler und Studierende, die sich auf Lektüre oder Prüfungen vorbereiten.

---

## Features

- 📄 **Texteingabe** – beliebigen lateinischen Text einfügen
- 🔍 **Automatische Abfrage** bei [Navigium](https://www.navigium.de) mit konfigurierbarer Thread-Anzahl für parallele Anfragen
- 🏷️ **Alle Wortarten** – Nomen, Verben, Adjektive, Pronomen, Präpositionen, Adverbien, Konjunktionen, Subjunktionen und Unbekannt
- 🔎 **Wortartenfilterung** – nur gewünschte Wortarten in die Liste aufnehmen
- 📖 **Bis zu 3 Bedeutungen** pro Vokabel (konfigurierbar)
- 🔬 **Klassenerkennung** – Deklinations- und Konjugationsklassen werden automatisch erkannt
- 📊 **Excel-Export** (`.xlsx`)
- 🃏 **Brainyoo-Export** (`.by2`) mit Lektionsname für Lernkarteikarten

---

## Installation

### Voraussetzungen

- Windows 10 oder neuer
- Aktive Internetverbindung (für Abfragen an Navigium)
- Python 3.12 *(nur bei Start aus dem Quellcode)*

### Option 1 – Fertige `.exe` (empfohlen)

Die neueste Version direkt aus dem [Releases-Bereich](https://github.com/Zwiebelrostbraten/Vokabulator/releases) herunterladen und installieren.

### Option 2 – Aus dem Quellcode
1. Repository klonen:
   ```bash
   git clone https://github.com/Zwiebelrostbraten/Vokabulator.git
   cd Vokabulator
   ```

2. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

3. Programm starten:
   ```bash
   python vokabel_gui.py
   ```
4. Bei 3. kann es sein, dass man die self.iconbitmap(default=sys.executable) aus der vokabel_gui.py löschen muss, damit es auserhalb der .exe funktioniert.

---

## Benutzung

1. Lateinischen Text in das **Texteingabe**-Feld einfügen
2. Gewünschte **Wortarten** über die Checkboxen auswählen (Nomen, Verben, Adjektive, ...)
3. **Anzahl der Bedeutungen** (1–3) über den Schieberegler einstellen
4. **Thread-Anzahl** für parallele Navigium-Abfragen bei Bedarf anpassen
5. Optional: **Brainyoo Export** aktivieren und einen Lektionsnamen eingeben
6. Auf **„Vokabeln generieren"** klicken und den Fortschritt in der Statusanzeige beobachten
7. Exportierte Datei (Excel oder `.by2`) in deiner Lern-App öffnen

---

## Geplante Features

* [ ] Brainyoo-Export mit bis zu drei Bedeutungen
* [ ] Integrierter PDF-Export bzw. insgesamt mehr Dateiformate

---

## Datenquelle

Die Vokabeldaten werden von [Navigium](https://www.navigium.de) abgerufen.

---

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).

---

*Entwickelt von [Zwiebelrostbraten](https://github.com/Zwiebelrostbraten)*
