# File name: lesson.py
# Author: Iivari Anttila
# Description: Class for the GUI for a lesson
from GUI.styleConstants import *
import tkinter as tk
from tkinter import ttk
import datetime

from learningProgress import LearningProgress
from target import Target
from targetTypes.word import Word
from targetTypes.grammarPoint import GrammarPoint
from targetTypes.conjugation import Conjugation
from targetTypes.phrase import Phrase

class Lesson(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.target:Target | None = None
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # Header
        header_frame = ttk.Frame(self, style="LessonHeader.TFrame")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.header = ttk.Label(
            header_frame,
            text="",
            style="LessonHeader.TLabel",
            anchor="center"
        )
        self.header.pack(pady=10)

        # Subheader
        subheader_frame = ttk.Frame(self, style="LessonHeader.TFrame")
        subheader_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.subheader = ttk.Label(
            subheader_frame,
            text="",
            style="LessonSubHeader.TLabel",
            anchor="center"
        )
        self.subheader.pack(pady=(10, 20))

        # Side Button Frame
        side_button_frame = ttk.Frame(self)
        side_button_frame.grid(row=2, column=0, pady=10, padx=(20, 0), sticky="s")

        # Side button 1 (Translation/Teaching Text)
        self.side1 = ttk.Button(
            side_button_frame,
            text="Side1",
            style="Custom.TButton",
            state="disabled",
            command = self.side1_pressed
        )
        self.side1.pack(side="top", pady=(0,10))

        # Side button 2 (Conjugations / Example Words)
        self.side2 = ttk.Button(
            side_button_frame,
            text="Side2",
            style="Custom.TButton",
            command=self.side2_pressed
        )
        self.side2.pack(side="top", pady=(0, 10))

        # Example sentences
        self.example_sentence_button = ttk.Button(
            side_button_frame,
            text="Ex. Sentences",
            style="Custom.TButton",
            command=self.show_example_sentences
        )
        self.example_sentence_button.pack(side="top", pady=(0, 10))

        # Bottom Button Frame
        bottom_button_frame = ttk.Frame(self)
        bottom_button_frame.grid(row=3, column=0, columnspan=2, pady=20, sticky="s")

        # Back Button
        button_back = ttk.Button(
            bottom_button_frame,
            text="Back",
            style="Custom.TButton",
            command=self.back
        )
        button_back.pack(side="left", padx=10)

        # Add Button
        self.button_submit = ttk.Button(
            bottom_button_frame,
            text="Add to Reviews",
            style="Custom.TButton",
            command=self.submit
        )
        self.button_submit.pack(side="left", padx=10)

        # Scrollable Content Frame
        container = ttk.Frame(self)
        container.grid(row=2, column=1, padx=(40, 0), pady=10, sticky="nsew")

        self.canvas = tk.Canvas(container, highlightthickness=0, height="190", width="400")
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.content_frame = ttk.Frame(self.canvas)

        self.content_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="y", expand=True)
        self.scrollbar.pack(side="left", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def update_user(self):
        self.target = self.controller.current_lesson
        self.set_header()
        self.set_subheader()
        self.set_side_buttons()
        self.side1_pressed()

    def set_header(self):
        header_text = ""
        if isinstance(self.target, Word):
            header_text = self.target.finnish_translations[0].capitalize()
        elif isinstance(self.target, GrammarPoint):
            header_text = self.target.english_translations[0].capitalize()

        self.header.config(text=header_text)

    def set_subheader(self):
        subheader_text = ""
        if isinstance(self.target, Word):
            subheader_text = self.target.english_translations[0].capitalize()
        elif isinstance(self.target, GrammarPoint):
            subheader_text = self.target.finnish_translations[0].capitalize()

        self.subheader.config(text=subheader_text)

    def set_side_buttons(self):
        if isinstance(self.target, Word):
            self.side1.config(text="Translations")
            self.side2.config(text="Conjugations")
        elif isinstance(self.target, GrammarPoint):
            self.side1.config(text="Information")
            self.side2.config(text="Ex. Words")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def submit(self):
        new_learning_progress = LearningProgress(
            self.target, 0, datetime.datetime.now().date()
        )
        self.controller.database.new_learning_progress(
            self.controller.current_user, new_learning_progress
        )
        self.controller.current_user.add_learning_progress(
            new_learning_progress
        )
        self.back()

    def back(self):
        self.controller.current_lesson = ""
        self.controller.show_frame("AllLessons")

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def side1_pressed(self):
        self.clear_content()
        self.side1.config(state="disabled")
        self.side2.config(state="enabled")
        self.example_sentence_button.config(state="enabled")
        if isinstance(self.target, Word):
            self.show_translations()
        elif isinstance(self.target, GrammarPoint):
            self.show_info()

    def side2_pressed(self):
        self.clear_content()
        self.side1.config(state="enabled")
        self.side2.config(state="disabled")
        self.example_sentence_button.config(state="enabled")
        if isinstance(self.target, Word):
            self.show_conjugations()
        elif isinstance(self.target, GrammarPoint):
            self.show_example_words()

    def show_translations(self):
        finnish_header = ttk.Label(
            self.content_frame,
            text="Finnish Translations",
            style="CustomBold.TLabel",
        )
        finnish_header.pack(side="top", pady=(10, 5), fill="x")

        finnish_translations = ttk.Label(
            self.content_frame,
            text=self.target.finnish_translations_string(),
            style="Custom.TLabel"
        )
        finnish_translations.pack(side="top", fill="x")

        english_header = ttk.Label(
            self.content_frame,
            text="English Translations",
            style="CustomBold.TLabel"
        )
        english_header.pack(side="top", pady=(30, 5), fill="x")

        english_translations = ttk.Label(
            self.content_frame,
            text=self.target.english_translations_string(),
            style="Custom.TLabel",
        )
        english_translations.pack(side="top", fill="x")

    def show_info(self):
        teaching_text = ttk.Label(
            self.content_frame,
            text=self.target.teaching_text,
            style="Custom.TLabel",
            wraplength="400",
            justify="left"
        )
        teaching_text.pack(side="top", pady=(10, 5), fill="x")

    def show_conjugations(self):
        bold_header = ttk.Label(
            self.content_frame,
            text="Conjugations",
            style="CustomBold.TLabel",
        )
        bold_header.pack(side="top", pady=(10, 5), fill="x")

        conjugations = ttk.Label(
            self.content_frame,
            text=self.target.conjugations_string(),
            style="Custom.TLabel"
        )
        conjugations.pack(side="top", fill="x")

    def show_example_words(self):
        conjugations = self.controller.database.get_grammar_conjugations(self.target)

        for conjugation in conjugations[:3]:
            finnish_translation = ttk.Label(
                self.content_frame,
                text=conjugation.finnish_translation,
                style="CustomBold.TLabel"
            )
            finnish_translation.pack(side="top", pady=(10, 5), fill="x")

            english_explanation = ttk.Label(
                self.content_frame,
                text=conjugation.english_string(),
                style="Custom.TLabel"
            )
            english_explanation.pack(side="top", fill="x")

        # If there are no conjugations
        if len(conjugations) == 0:
            label = ttk.Label(
                self.content_frame,
                text="No example words available. (Sorry)",
                style="Custom.TLabel"
            )
            label.pack(side="top", fill="x")

    def show_example_sentences(self):
        self.clear_content()
        self.side1.config(state="enabled")
        self.side2.config(state="enabled")
        self.example_sentence_button.config(state="disabled")
        phrases = []
        if isinstance(self.target, Word):
            phrases = self.controller.database.get_word_phrases(self.target)
        elif isinstance(self.target, GrammarPoint):
            phrases = self.controller.database.get_grammar_phrases(self.target)

        # Set phrases
        for phrase in phrases[:3]:

            phrase_finnish = ttk.Label(
                self.content_frame,
                text=phrase.finnish_translations[0],
                style="CustomBold.TLabel",
            )
            phrase_finnish.pack(side="top", pady=(10, 5), fill="x")

            phrase_english = ttk.Label(
                self.content_frame,
                text=phrase.english_translations[0],
                style="Custom.TLabel"
            )
            phrase_english.pack(side="top", fill="x")

        # If phrase amount is 0
        if len(phrases) == 0:
            label = ttk.Label(
                self.content_frame,
                text="No example phrases available. (Sorry)",
                style="Custom.TLabel"
            )
            label.pack(side="top", fill="x")