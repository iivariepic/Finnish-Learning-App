# File name: reviews.py
# Author: Iivari Anttila
# Description: Class for the GUI of reviewing targets

from GUI.styleConstants import *
import tkinter as tk
from tkinter import ttk
from targetTypes.grammarPoint import GrammarPoint
from targetTypes.word import Word
import random

class Reviews(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user = None
        self.remaining_reviews = []
        self.mistakes:set = set([])
        self.completed = []
        self.current_learning_progress = None
        self.current_target = None
        self.state = "guess" # guess or result
        self.phrase = None
        self.phrase_word = None
        self.phrase_conjugation = None

        # Header (Usually finnish targetTypes)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.header = ttk.Label(self, text="Placeholder", font=HEADER_FONT, anchor="center")
        self.header.grid(row=0, column=0, pady=20, sticky="nsew")

        # What to type?-label
        self.instructions = ttk.Label(
            self,
            text="Type the English Translation:",
            style="Custom.TLabel",
            anchor="center"
        )
        self.instructions.grid(row=1, column=0, sticky="ew")

        # The input box
        self.user_input = tk.StringVar()
        user_entry = ttk.Entry(
            self,
            textvariable=self.user_input,
            justify="center",
            style="Custom.TEntry")
        user_entry.grid(row=2, column=0, padx=20, sticky="ew")

        # Bind enter to the submit answer function
        user_entry.bind("<Return>", lambda event: self.submit_answer())

        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, pady=20)

        # Back button
        back_button = ttk.Button(
            button_frame,
            text="Back",
            style="Custom.TButton",
            command=self.back
        )
        back_button.pack(side="left", padx=10)

        # Sumbit Answer button
        self.submit_button = ttk.Button(
            button_frame,
            text="Submit",
            style="Custom.TButton",
            command=self.submit_answer
        )
        self.submit_button.pack(side="left", padx=10)

        # Correct Answer Button
        self.correct_button = ttk.Button(
            button_frame,
            text="Correct Answer",
            style="Custom.TButton",
            command=self.correct_answer,
            state="disabled"
        )
        self.correct_button.pack(side="left", padx=10)


    def save_progress(self):
        for learning_progress in self.completed:
            if learning_progress in self.mistakes:
                learning_progress.update_progress(False)
            else:
                learning_progress.update_progress(True)

            self.controller.database.change_learning_progress(self.user, learning_progress)

        # Reset state
        self.state = "guess"
        self.submit_button.config(text="Submit")
        self.header.config(style="Custom.TLabel")

    def set_target(self):
        # Go back if review pile is empty:
        if len(self.remaining_reviews) == 0:
            self.back()
            return

        self.current_target = self.remaining_reviews[0].target
        self.current_learning_progress = self.remaining_reviews[0]

        # If target is word
        if isinstance(self.current_target, Word):
            self.header.config(text=f"{self.current_target.finnish_translations[0]}".capitalize())
            self.instructions.config(text="Type the English Translation")

        # If target is grammar point
        elif isinstance(self.current_target, GrammarPoint):
            self.phrase = self.select_grammar_phrase(self.current_target)

            # Get the answer word
            for word in self.phrase.words:
                for conjugation in word.conjugations:
                    if conjugation.required_grammar.target_id == self.current_target.target_id:
                        self.phrase_word = word
                        self.phrase_conjugation = conjugation

            # Set the header text
            header_text = self.phrase.finnish_translations[0].replace(
                self.phrase_conjugation.finnish_translation,
                "__"
            )
            header_text += f" ({self.phrase_word.finnish_translations[0]})"
            self.header.config(text=header_text)

            # Set the instructions text
            instructions_text = f"Conjugate {self.phrase_word} into"

            if self.phrase_word.part_of_speech == "Adjective":
                instructions_text += f" {phrase_conjugation.comparison_degree}"

            elif self.phrase_word.part_of_speech == "Verb":
                instructions_text += f" {self.phrase_conjugation.tense}"

            instructions_text += f" {self.phrase_conjugation.type}"
            self.instructions.config(text=instructions_text)

    def update_user(self):
        self.user = self.controller.current_user
        self.remaining_reviews = self.controller.get_reviews()
        random.shuffle(self.remaining_reviews)
        self.set_target()
        self.mistakes.clear()
        self.completed.clear()

    def back(self):
        self.save_progress()

        # Update the homepage
        home_page = self.controller.frames["HomePage"]
        home_page.update_user()

        self.controller.show_frame("HomePage")

    def submit_answer(self):
        if self.state == "guess":
            self.result()
            self.user_input.set("")

        elif self.state == "result":
            self.go_to_next()

    def correct_answer(self):
        header_text = self.header.cget("text")
        if isinstance(self.current_target, Word):
            header_text += f" = {self.get_correct_answer()[0].capitalize()}"

        elif isinstance(self.current_target, GrammarPoint):
            header_text = self.phrase.finnish_translations[0]

        self.header.config(text=header_text)
        self.correct_button.config(state="disabled")

    def result(self):
        self.state = "result"
        self.submit_button.config(text="Continue")
        self.correct_button.config(state="enabled")

        if self.check_answer():
            self.header.config(style="ReviewCorrect.TLabel")
            self.completed.append(self.current_learning_progress)
            self.remaining_reviews.remove(self.current_learning_progress)
        else:
            self.header.config(style="ReviewWrong.TLabel")
            self.mistakes.add(self.current_learning_progress)
            random.shuffle(self.remaining_reviews)

    def go_to_next(self):
        self.state = "guess"
        self.phrase = None
        self.phrase_word = None
        self.phrase_conjugation = None
        self.submit_button.config(text="Submit")
        self.header.config(style="Custom.TLabel")
        self.correct_button.config(state="disabled")
        self.set_target()

    def check_answer(self):
        return self.user_input.get().casefold() in self.get_correct_answer()

    def get_correct_answer(self):
        if isinstance(self.current_target, Word):
            return self.current_target.english_translations

        if isinstance(self.current_target, GrammarPoint):
            return [self.phrase_conjugation.finnish_translation]


    def select_grammar_phrase(self, grammar_point:GrammarPoint):
        phrases = self.controller.database.get_grammar_phrases(grammar_point)

        if not phrases:
            return

        phrases_with_user_words = []
        for phrase in phrases:
            for learning_progress in self.user.learning_progresses:
                if learning_progress.target in phrase.words:
                    phrases_with_user_words.append(phrase)

        if phrases_with_user_words:
            random.shuffle(phrases_with_user_words)
            return phrases_with_user_words[0]

        random.shuffle(phrases)
        return phrases[0]