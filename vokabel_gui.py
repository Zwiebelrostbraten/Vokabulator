import customtkinter as ctk
import threading
import time
import webbrowser
from tkinter import filedialog, messagebox
import navigium_mit_Textbelgen as navigium

class VokabelGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.iconbitmap(default=sys.executable)

        # Fenster Setup
        self.title("Vokabulator")
        self.geometry("1000x750")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Variablen für generierte Daten
        self.excel_data = None
        self.vocabulary_data = None

        # --- MENÜLEISTE ---
        self.create_menu()

        # --- MAIN CONTENT ---
        self.main_container = ctk.CTkFrame(self)
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # === LINKE SEITE: Eingabe ===
        self.input_frame = ctk.CTkFrame(self.main_container)
        self.input_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(1, weight=1)

        # Titel
        title_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        ctk.CTkLabel(title_frame, text="📝 Texteingabe", 
                     font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")

        # Textfeld
        self.textbox = ctk.CTkTextbox(self.input_frame, corner_radius=8, 
                                      font=ctk.CTkFont(size=14))
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Optionen Bereich
        options_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        options_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        options_frame.grid_columnconfigure(0, weight=1)
        options_frame.grid_columnconfigure(1, weight=1)
        
        # --- SPALTE 1: Export, Threads & Bedeutungen ---
        left_options = ctk.CTkFrame(options_frame, fg_color="transparent")
        left_options.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left_options.grid_columnconfigure(0, weight=1)

        # 1. Brainyoo Export Checkbox
        self.check_brainyoo = ctk.CTkCheckBox(left_options, text="Brainyoo Export (.by2)", 
                                              command=self.toggle_brainyoo_options,
                                              font=ctk.CTkFont(size=14))
        self.check_brainyoo.grid(row=0, column=0, sticky="w", pady=(5, 0))

        # 2. Brainyoo Lektionsname (GEÄNDERT: Immer sichtbar, aber ggf. disabled)
        # Wir reservieren den Platz fest, damit nichts "springt"
        self.brainyoo_frame = ctk.CTkFrame(left_options, fg_color="transparent")
        self.brainyoo_frame.grid(row=1, column=0, sticky="ew", pady=(2, 10)) 
        
        self.lektion_entry = ctk.CTkEntry(self.brainyoo_frame, placeholder_text="Lektionsname (entspricht i. d. R. Titel des lat. Textes)",
                                          font=ctk.CTkFont(size=14)) # Visuell etwas ausgegraut
        self.lektion_entry.pack(fill="x")

        # 3. Thread Control Label
        thread_label = ctk.CTkLabel(left_options, text="Threads:", anchor="w",
                                    font=ctk.CTkFont(size=14))
        thread_label.grid(row=2, column=0, sticky="w", pady=(5, 2))

        # 4. Thread Control Slider
        thread_control = ctk.CTkFrame(left_options, fg_color="transparent")
        thread_control.grid(row=3, column=0, sticky="ew")
        
        self.slider_threads = ctk.CTkSlider(thread_control, from_=1, to=128, number_of_steps=127,
                                            command=self.on_slider_threads_change)
        self.slider_threads.set(64)
        self.slider_threads.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.thread_entry = ctk.CTkEntry(thread_control, width=50, justify="center",
                                         font=ctk.CTkFont(size=14))
        self.thread_entry.insert(0, "64")
        self.thread_entry.bind("<KeyRelease>", self.on_thread_entry_change)
        self.thread_entry.bind("<FocusOut>", self.validate_thread_entry)
        self.thread_entry.pack(side="right")

        # 5. Bedeutungen Label
        meanings_label = ctk.CTkLabel(left_options, text="Anzahl Bedeutungen (1-3):", anchor="w",
                                      font=ctk.CTkFont(size=14))
        meanings_label.grid(row=4, column=0, sticky="w", pady=(10, 2))

        # 6. Bedeutungen Control Slider
        meanings_control = ctk.CTkFrame(left_options, fg_color="transparent")
        meanings_control.grid(row=5, column=0, sticky="ew")

        self.slider_meanings = ctk.CTkSlider(meanings_control, from_=1, to=3, number_of_steps=2,
                                             command=self.on_slider_meanings_change)
        self.slider_meanings.set(1)
        self.slider_meanings.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.meanings_entry = ctk.CTkEntry(meanings_control, width=50, justify="center",
                                           font=ctk.CTkFont(size=14))
        self.meanings_entry.insert(0, "1")
        self.meanings_entry.bind("<KeyRelease>", self.on_meanings_entry_change)
        self.meanings_entry.bind("<FocusOut>", self.validate_meanings_entry)
        self.meanings_entry.pack(side="right")


        # --- SPALTE 2: Wortarten Filter ---
        filter_frame = ctk.CTkFrame(options_frame, fg_color=("gray85", "gray20"), corner_radius=6)
        filter_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), rowspan=6)
        
        ctk.CTkLabel(filter_frame, text="Wortarten filtern", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=2)

        self.var_all = ctk.BooleanVar(value=False)
        self.chk_all = ctk.CTkCheckBox(filter_frame, text="Alle", variable=self.var_all, 
                                       command=self.toggle_all_wordtypes, font=ctk.CTkFont(size=12, weight="bold"))
        self.chk_all.pack(anchor="w", padx=10, pady=2)

        self.wordtype_grid = ctk.CTkFrame(filter_frame, fg_color="transparent")
        self.wordtype_grid.pack(fill="both", expand=True, padx=5, pady=2)

        self.wordtype_vars = {
            "Nomen": ctk.BooleanVar(value=True),
            "Verben": ctk.BooleanVar(value=True),
            "Adjektive": ctk.BooleanVar(value=True),
            "Pronomen": ctk.BooleanVar(value=False),
            "Präpositionen": ctk.BooleanVar(value=False),
            "Adverbien": ctk.BooleanVar(value=False),
            "Konjunktionen": ctk.BooleanVar(value=False),
            "Subjunktionen": ctk.BooleanVar(value=False),
            "Unbekannt": ctk.BooleanVar(value=False)
        }
        
        self.wordtype_checkboxes = {}
        row = 0
        col = 0
        for name, var in self.wordtype_vars.items():
            cb = ctk.CTkCheckBox(self.wordtype_grid, text=name, variable=var, 
                                 font=ctk.CTkFont(size=11), width=80, height=20,
                                 state="normal") 
            cb.grid(row=row, column=col, sticky="w", padx=2, pady=2)
            self.wordtype_checkboxes[name] = cb
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.btn_submit = ctk.CTkButton(self.input_frame, text="🚀 Vokabeln generieren", 
                                        command=self.start_processing_thread, height=40,
                                        font=ctk.CTkFont(size=12, weight="bold"))
        self.btn_submit.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

        # === RECHTE SEITE: Ergebnisse ===
        self.output_frame = ctk.CTkFrame(self.main_container)
        self.output_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(3, weight=1)

        result_title = ctk.CTkFrame(self.output_frame, fg_color="transparent")
        result_title.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        ctk.CTkLabel(result_title, text="📊 Status", 
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")

        self.progress_bar = ctk.CTkProgressBar(self.output_frame)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 5))

        self.status_label = ctk.CTkLabel(self.output_frame, text="Bereit", anchor="w",
                                         font=ctk.CTkFont(size=14))
        self.status_label.grid(row=2, column=0, sticky="ew", padx=10, pady=(30, 10))

        self.result_textbox = ctk.CTkTextbox(self.output_frame, height=200, state="disabled",
                                             font=ctk.CTkFont(size=12))
        self.result_textbox.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.download_frame = ctk.CTkFrame(self.output_frame, fg_color="transparent")
        
        self.btn_download_excel = ctk.CTkButton(self.download_frame, text="💾 Excel speichern", 
                                                command=self.download_excel, height=36, 
                                                fg_color="#2fa572", hover_color="#1f8456",
                                                font=ctk.CTkFont(size=14))
        self.btn_download_excel.pack(fill="x", pady=3)
        
        self.btn_download_by2 = ctk.CTkButton(self.download_frame, text="💾 Brainyoo speichern", 
                                              command=self.download_by2, height=36,
                                              fg_color="#d97706", hover_color="#b45309",
                                              font=ctk.CTkFont(size=14))
        self.btn_download_by2.pack(fill="x", pady=3)

        self.statusbar = ctk.CTkFrame(self, height=25, fg_color=("gray90", "gray13"))
        self.statusbar.grid(row=2, column=0, sticky="ew")
        self.statusbar_label = ctk.CTkLabel(self.statusbar, 
                                            text="Version 1.2.1 | Alle Wortarten + bis zu 3 Bedeutungen + Wortartenfilterung", 
                                            font=ctk.CTkFont(size=12))
        self.statusbar_label.pack(side="left", padx=10)
        self.toggle_brainyoo_options()

    # --- Hilfsfunktionen für Wortarten ---
    def toggle_all_wordtypes(self):
        is_all = self.var_all.get()
        state = "disabled" if is_all else "normal"
        for name, cb in self.wordtype_checkboxes.items():
            cb.configure(state=state)
            if is_all:
                self.wordtype_vars[name].set(True)

    def get_selected_wordtypes(self):
        if self.var_all.get():
            return {name: True for name in self.wordtype_vars}
        else:
            return {name: var.get() for name, var in self.wordtype_vars.items()}

    # --- Hilfsfunktionen für Slider: Threads ---
    def on_slider_threads_change(self, value):
        thread_value = int(value)
        self.thread_entry.delete(0, "end")
        self.thread_entry.insert(0, str(thread_value))

    def on_thread_entry_change(self, event):
        try:
            value = int(self.thread_entry.get())
            if 1 <= value <= 128:
                self.slider_threads.set(value)
        except ValueError:
            pass

    def validate_thread_entry(self, event):
        try:
            value = int(self.thread_entry.get())
            value = max(1, min(128, value))
            self.thread_entry.delete(0, "end")
            self.thread_entry.insert(0, str(value))
            self.slider_threads.set(value)
        except ValueError:
            current_slider = int(self.slider_threads.get())
            self.thread_entry.delete(0, "end")
            self.thread_entry.insert(0, str(current_slider))

    # --- Hilfsfunktionen für Slider: Bedeutungen ---
    def on_slider_meanings_change(self, value):
        meanings_value = int(value)
        self.meanings_entry.delete(0, "end")
        self.meanings_entry.insert(0, str(meanings_value))

    def on_meanings_entry_change(self, event):
        try:
            value = int(self.meanings_entry.get())
            if 1 <= value <= 3:
                self.slider_meanings.set(value)
        except ValueError:
            pass

    def validate_meanings_entry(self, event):
        try:
            value = int(self.meanings_entry.get())
            value = max(1, min(3, value))
            self.meanings_entry.delete(0, "end")
            self.meanings_entry.insert(0, str(value))
            self.slider_meanings.set(value)
        except ValueError:
            current_slider = int(self.slider_meanings.get())
            self.meanings_entry.delete(0, "end")
            self.meanings_entry.insert(0, str(current_slider))

    def create_menu(self):
        """Erstellt eine Menüleiste"""
        menubar = ctk.CTkFrame(self, height=30, fg_color=("gray85", "gray15"))
        menubar.grid(row=0, column=0, sticky="ew")
        
        # Hilfe-Menü
        help_btn = ctk.CTkButton(menubar, text="📖 Hilfe", width=70, height=25,
                                 fg_color="transparent", hover_color=("gray75", "gray25"),
                                 command=self.show_help, font=ctk.CTkFont(size=14))
        help_btn.pack(side="left", padx=5, pady=2)
        
        # Info-Menü
        info_btn = ctk.CTkButton(menubar, text="ℹ️ Info", width=70, height=25,
                                fg_color="transparent", hover_color=("gray75", "gray25"),
                                command=self.show_info, font=ctk.CTkFont(size=14))
        info_btn.pack(side="left", padx=5, pady=2)
        
        # GitHub
        github_btn = ctk.CTkButton(menubar, text="💻 GitHub", width=70, height=25,
                                   fg_color="transparent", hover_color=("gray75", "gray25"),
                                   command=lambda: webbrowser.open("https://github.com/Zwiebelrostbraten/Vokabulator"),
                                   font=ctk.CTkFont(size=14))
        github_btn.pack(side="left", padx=5, pady=2)
    
    def show_help(self):
        """Zeigt Hilfe-Dialog"""
        help_window = ctk.CTkToplevel(self)
        help_window.title("Hilfe")
        help_window.geometry("550x450")
        help_window.transient(self)
        help_window.grab_set()
        
        # Scrollable Textbox
        text = ctk.CTkTextbox(help_window, wrap="word", font=ctk.CTkFont(size=14))
        text.pack(fill="both", expand=True, padx=15, pady=(15, 10))
        
        help_text = """VOKABULATOR - ANLEITUNG

1. TEXTEINGABE
   Füge deinen lateinischen Text in das linke Textfeld ein.

2. OPTIONEN
   • Brainyoo Export: Aktiviere diese Option, um eine .by2 Datei 
     für Brainyoo zu erstellen. Gib dann einen Lektionsnamen ein.
   
   • Threads: Mehr Threads = schnellere Verarbeitung
     Empfohlen: 32-64 Threads

3. VERARBEITUNG
   Klicke auf "Vokabeln generieren" und warte auf die Fertigstellung.

4. DOWNLOAD
   Nach der Verarbeitung erscheinen Download-Buttons.
   Wähle den Speicherort für deine Dateien.

HINWEISE
• Aktuell werden nur Nomen, Verben und Adjektive extrahiert
• Die Verarbeitung kann je nach Textlänge 10-60 Sekunden dauern
• Excel-Dateien können in Brainyoo, Anki und anderen Tools 
  importiert werden
"""
        text.insert("1.0", help_text)
        text.configure(state="disabled")
        
        # Brainyoo Tutorial Button
        btn_frame = ctk.CTkFrame(help_window, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        brainyoo_btn = ctk.CTkButton(btn_frame, 
                                     text="🔗 Brainyoo Import-Tutorial öffnen",
                                     command=lambda: webbrowser.open("https://brainyoo.de/dokumentation/xml-die-browser-version/der-xml-reimport/"),
                                     font=ctk.CTkFont(size=14))
        brainyoo_btn.pack(side="left", expand=True, fill="x", padx=5)
        
        close_btn = ctk.CTkButton(btn_frame, text="Schließen", 
                                 command=help_window.destroy,
                                 font=ctk.CTkFont(size=14))
        close_btn.pack(side="right", padx=5)

    def show_info(self):
        """Zeigt Info-Dialog mit Disclaimer und Datenschutz"""
        info_window = ctk.CTkToplevel(self)
        info_window.title("Informationen")
        info_window.geometry("550x500")
        info_window.transient(self)
        info_window.grab_set()
        
        text = ctk.CTkTextbox(info_window, wrap="word", font=ctk.CTkFont(size=14))
        text.pack(fill="both", expand=True, padx=15, pady=(15, 10))
        
        info_text = """VOKABULATOR GENERATOR

Version: 1.2.1
Programmiert von: Rostbraten
GitHub: https://github.com/Zwiebelrostbraten/Vokabulator

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DISCLAIMER / HAFTUNGSAUSSCHLUSS

Diese Software wird "wie besehen" bereitgestellt, ohne jegliche 
Gewährleistung. Die Nutzung erfolgt auf eigene Verantwortung.

• Korrektheit: Die generierten Vokabellisten basieren auf Daten 
  von navigium.de. Fehler in den Übersetzungen oder bei der 
  Worterkennung können nicht ausgeschlossen werden.

• Keine Haftung: Der Autor übernimmt keine Haftung für Schäden, 
  die durch die Nutzung dieser Software entstehen.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DATENSCHUTZ

• Lokale Verarbeitung: Alle Daten werden lokal auf deinem 
  Computer verarbeitet.

• Navigium-Anfragen: Zur Übersetzung werden Anfragen an 
  navigium.de gesendet. Dabei werden nur einzelne Wörter 
  übertragen, keine vollständigen Texte.

• Keine Speicherung: Diese Anwendung speichert keine Nutzerdaten, 
  Texte oder Verlaufsinformationen.

• Keine Weitergabe: Deine Eingaben werden nicht an Dritte 
  weitergegeben (außer den notwendigen Anfragen an navigium.de).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERWENDETE DIENSTE

• Navigium (navigium.de): Latein-Wörterbuch und Formbestimmung
  Die Nutzung von navigium.de unterliegt deren Nutzungsbedingungen.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LIZENZ

MIT - Details siehe GitHub Repository
"""
        text.insert("1.0", info_text)
        text.configure(state="disabled")
        
        # Schließen Button
        close_btn = ctk.CTkButton(info_window, text="Schließen", 
                                 command=info_window.destroy,
                                 font=ctk.CTkFont(size=14))
        close_btn.pack(pady=(0, 15))

    # GEÄNDERT: Schaltet nur noch den Status um, nicht mehr das Grid
    def toggle_brainyoo_options(self):
        if self.check_brainyoo.get():
            # Aktiviert: Helles/Dunkles Eingabefeld (Standardfarben für Entry)
            self.lektion_entry.configure(
                state="normal", 
                fg_color=["#F9F9FA", "#343638"],  # Standard Entry-Farben (Light/Dark Mode)
                border_color=["#979DA2", "#565B5E"], # Standard Rahmen
                text_color=["gray14", "gray84"]   # Standard Text
            )
        else:
            # Deaktiviert: Graues Feld (statt transparent)
            self.lektion_entry.configure(
                state="disabled", 
                fg_color=["gray90", "gray20"],    # Fester Grauwert statt "transparent"
                border_color=["gray80", "gray30"], # Rahmen etwas dunkler machen
                text_color=["gray60", "gray40"]   # Text ausgrauen
            )


    # --- Verarbeitung ---
    def start_processing_thread(self):
        input_text = self.textbox.get("1.0", "end-1c")
        if not input_text.strip():
            messagebox.showwarning("Eingabe fehlt", "Bitte geben Sie einen lateinischen Text ein!")
            return
        
        wordtype_filter = self.get_selected_wordtypes()
        if not any(wordtype_filter.values()):
            messagebox.showwarning("Auswahl fehlt", "Bitte wählen Sie mindestens eine Wortart aus!")
            return
        
        if self.check_brainyoo.get():
            lektion_name = self.lektion_entry.get().strip()
            if not lektion_name:
                messagebox.showwarning("Lektionsname fehlt", "Für den Brainyoo-Export müssen Sie einen Lektionsnamen angeben!")
                self.lektion_entry.focus() # Setzt den Cursor direkt ins Feld
                return
        
        self.validate_thread_entry(None)
        self.validate_meanings_entry(None)

        self.btn_submit.configure(state="disabled", text="⏳ Verarbeite...")
        self.progress_bar.set(0)
        self.download_frame.grid_forget()
        self.log_message("Verarbeitung gestartet")
        
        export2by = bool(self.check_brainyoo.get())
        lektion_name = self.lektion_entry.get().strip() if export2by else ""
        
        threads = int(self.thread_entry.get())
        anzahl_bedeutungen = int(self.meanings_entry.get())

        thread = threading.Thread(target=self.run_logic, 
                                  args=(input_text, export2by, lektion_name, threads, wordtype_filter, anzahl_bedeutungen))
        thread.start()

    def update_progress(self, val, desc):
        self.after(0, lambda: self._update_ui_progress(val, desc))

    def _update_ui_progress(self, val, desc):
        self.progress_bar.set(val)
        self.status_label.configure(text=desc)

    def log_message(self, msg):
        self.after(0, lambda: self._append_log(msg))

    def _append_log(self, msg):
        self.result_textbox.configure(state="normal")
        timestamp = time.strftime("%H:%M:%S")
        self.result_textbox.insert("end", f"[{timestamp}] {msg}\n")
        self.result_textbox.configure(state="disabled")
        self.result_textbox.see("end")

    def processing_finished(self, count, duration, has_by2):
        self.after(0, lambda: self._finish_ui(count, duration, has_by2))

    def _finish_ui(self, count, duration, has_by2):
        self.btn_submit.configure(state="normal", text="🚀 Vokabeln generieren")
        self.progress_bar.set(1)
        self.status_label.configure(text="✓ Fertig!")
        self.log_message(f"Abgeschlossen in {duration:.1f}s - {count} Vokabeln")
        
        self.download_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        
        if has_by2:
            self.btn_download_by2.pack(fill="x", pady=3)
        else:
            self.btn_download_by2.pack_forget()

    def download_excel(self):
        if self.vocabulary_data is None:
            self.log_message("Keine Daten verfügbar")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Dateien", "*.xlsx")],
            initialfile="Vokabelliste.xlsx"
        )
        if filepath:
            try:
                navigium.save2excel(filepath, self.vocabulary_data)
                self.log_message(f"Excel gespeichert")
            except Exception as e:
                self.log_message(f"Fehler: {str(e)}")

    def download_by2(self):
        if self.excel_data is None:
            self.log_message("Keine Daten verfügbar")
            return
        
        lektion_name = self.lektion_entry.get().strip()
        initial_filename = f"{lektion_name}.by2" if lektion_name else "Vokabelliste.by2"
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".by2",
            filetypes=[("Brainyoo Dateien", "*.by2")],
            initialfile=initial_filename
        )
        if filepath:
            try:
                navigium.save2by2(self.excel_data, filepath)
                self.log_message(f"Brainyoo gespeichert")
            except Exception as e:
                self.log_message(f"Fehler: {str(e)}")

    def run_logic(self, input_text, export2by, lektion_name, anzahl_threads, wordtype_filter, anzahl_bedeutungen):
        start_time = time.time()
        
        try:
            self.update_progress(0.05, "Vorbereitung...")
            text_lines = input_text.split("\n")
            words = navigium.split_into_words(text_lines)

            self.update_progress(0.1, "Navigium-Anfrage...")
            output = navigium.threaded_function(words, anzahl_threads=anzahl_threads)

            self.update_progress(0.61, "Sortiere Wortarten...")
            sorted_data = navigium.sort_by_wordtype(output)
            
            vocabulary = navigium.advanced_formating(sorted_data, anzahl_bedeutungen=anzahl_bedeutungen, **wordtype_filter)

            self.update_progress(0.83, "Erstelle Dateien...")
            
            self.vocabulary_data = vocabulary
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                temp_path = tmp.name
            
            self.excel_data = navigium.save2excel(temp_path, vocabulary)
            
            anzahl = sum(len(liste) for liste in vocabulary.values())
            end_time = time.time()
            duration = end_time - start_time

            self.processing_finished(anzahl, duration, export2by)

        except Exception as e:
            self.log_message(f"FEHLER: {str(e)}")
            self.after(0, lambda: self.btn_submit.configure(state="normal", text="🚀 Vokabeln generieren"))

if __name__ == "__main__":
    app = VokabelGeneratorApp()
    app.mainloop()
