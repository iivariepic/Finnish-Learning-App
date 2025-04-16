# File name: lesson.py
# Author: Iivari Anttila
# Description: Class for the GUI for a lesson
from GUI.styleConstants import *
import tkinter as tk
from tkinter import ttk
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
        side_button_frame.grid(row=2, rowspan=2 , column=0, pady=10, padx=(20, 0), sticky="s")

        # Side button 1 (Translation/Teaching Text)
        self.side1 = ttk.Button(
            side_button_frame,
            text="Side1",
            style="Custom.TButton",
            command = self.side1_pressed
        )
        self.side1.pack(side="top", pady=(0,10))

        # Side button 2 ((Example) conjugations)
        self.side2 = ttk.Button(
            side_button_frame,
            text="Side2",
            style="Custom.TButton",
            command=self.side2_pressed
        )
        self.side2.pack(side="top", pady=(0, 10))

        # Example sentences
        example_sentence_button = ttk.Button(
            side_button_frame,
            text="Ex. Sentences",
            style="Custom.TButton",
            command=self.show_example_sentences
        )
        example_sentence_button.pack(side="top", pady=(0, 10))

        # Bottom Button Frame
        bottom_button_frame = ttk.Frame(self)
        bottom_button_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky="s")

        # Back Button
        button_back = ttk.Button(
            bottom_button_frame,
            text="Back",
            style="Custom.TButton",
            command=self.back
        )
        button_back.pack(side="left", padx=20)

        # Add Button
        self.button_submit = ttk.Button(
            bottom_button_frame,
            text="Add to Reviews",
            state="disabled",
            style="Custom.TButton",
            command=self.submit
        )
        self.button_submit.pack(side="left", padx=20)

    def update_user(self):
        self.target = self.controller.current_lesson
        self.set_header()
        self.set_subheader()

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

    def submit(self):
        self.back()

    def back(self):
        self.controller.current_lesson = ""
        self.controller.show_frame("AllLessons")

    def side1_pressed(self):
        print(self)
        print("Side1")

    def side2_pressed(self):
        print(self)
        print("Side2")

    def show_example_sentences(self):
        print(self)
        print("Example sentences")