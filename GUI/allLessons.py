# File name: allLessons.py
# Author: Iivari Anttila
# Description: A class for the GUI of selecting a lesson
from GUI.styleConstants import *
import tkinter as tk
from tkinter import ttk

from target import Target
from user import User
from targetTypes.grammarPoint import GrammarPoint
from targetTypes.word import Word

class AllLessons(ttk.Frame):
    TARGETS_PER_ROW = 4

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user = None
        self.available_words:list[Word] = []
        self.available_grammar:list[GrammarPoint] = []
        self.filtered_targets:list = []
        self.current_page = 0
        self.showing = "word"

        self.columnconfigure(0, weight=1)

        target_type_button_frame = ttk.Frame(self)
        target_type_button_frame.grid(row=0, column=0, pady=20)
        # Button to show Words (selected by default)
        self.word_button = ttk.Button(
            target_type_button_frame,
            text="Show Words",
            style="Custom.TButton",
            command=self.show_words,
            state="disabled"
        )
        self.word_button.pack(side="left", padx=10)

        # Button to show Grammar Points
        self.grammar_button = ttk.Button(
            target_type_button_frame,
            text="Show Grammar",
            style="Custom.TButton",
            command=self.show_grammar
        )
        self.grammar_button.pack(side="left", padx=10)

        # Target Button Frames
        self.target_button_row1 = ttk.Frame(self, height=50)
        self.target_button_row1.grid(row=1, column=0, pady=10)
        self.target_button_row1.grid_propagate(False)

        self.target_button_row2 = ttk.Frame(self, height=50)
        self.target_button_row2.grid(row=2, column=0, pady=10)
        self.target_button_row2.grid_propagate(False)

        # "Page" navigation buttons
        navigation_frame = ttk.Frame(self)
        navigation_frame.grid(row=3, column=0, pady=10)
        self.button_previous = ttk.Button(
            navigation_frame,
            text="←",
            command=lambda: self.change_page_by(-1),
            style="Arrow.TButton"
        )

        self.button_middle_label = ttk.Label(
            navigation_frame,
            text=f"{self.current_page + 1}/{len(self.filtered_targets) // 5 + 1}",
            font=CONTENT_FONT
        )

        self.button_next = ttk.Button(
            navigation_frame,
            text="→",
            command=lambda: self.change_page_by(1),
            style="Arrow.TButton"
        )

        self.button_previous.pack(side="left", padx=10)
        self.button_middle_label.pack(side="left", padx=10)
        self.button_next.pack(side="left", padx=10)

        # Searching
        search_frame = ttk.Frame(self)
        search_frame.grid(row=4, column=0, pady=20, padx=20, sticky="ew")

        search_label = ttk.Label(
            search_frame,
            text="Search:",
            style="Custom.TLabel"
        )
        search_label.pack(side="left", padx=10)

        # Search Entry
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, style="Custom.TEntry")
        search_entry.pack(side="left", fill=tk.X, expand=1, padx=(0, 40))
        search_entry.bind("<KeyRelease>", self.on_search)

        # Back Button
        back_button = ttk.Button(
            self,
            text="Back",
            style="Custom.TButton",
            command=self.back
        )
        back_button.grid(row=5, column=0, sticky="ew", padx=20)

    def update_user(self):
        self.user = self.controller.current_user
        self.show_words()
        self.search_var.set("")

        all_targets = self.controller.get_unlearned_targets()
        self.available_words = [
            target for target in all_targets if isinstance(target, Word)
        ]
        self.available_grammar = [
            target for target in all_targets if isinstance(target, GrammarPoint)
        ]
        self.filtered_targets = self.available_words
        self.update_target_buttons()

    def show_words(self):
        self.grammar_button.config(state="enabled")
        self.word_button.config(state="disabled")
        self.showing = "word"
        self.on_search()

    def show_grammar(self):
        self.word_button.config(state="enabled")
        self.grammar_button.config(state="disabled")
        self.showing = "grammar"
        self.on_search()

    def update_target_buttons(self):
        # Clear the old buttons
        for widget in self.target_button_row1.winfo_children():
            widget.destroy()

        for widget in self.target_button_row2.winfo_children():
            widget.destroy()

        start = self.current_page * self.TARGETS_PER_ROW
        end = start + self.TARGETS_PER_ROW
        page_targets = self.filtered_targets[start:end]

        target_index = 0
        for target in page_targets:
            if target_index < 4:
                self.target_button(target, self.target_button_row1)
            else:
                self.target_button(target, self.target_button_row2)

            target_index += 1

        # Display text if nothing is found
        if len(page_targets) == 0:
            label = ttk.Label(
                self.target_button_row1,
                text="Nothing found here!",
                style="CustomBold.TLabel"
            )
            label.pack()

        # Disable navigation buttons at page boundaries
        self.button_previous.config(state="normal" if self.current_page > 0 else "disabled")
        self.button_middle_label.config(
            text=f"{self.current_page + 1}/{len(self.filtered_targets) // self.TARGETS_PER_ROW + 1}"
        )
        self.button_next.config(state="normal" if end < len(self.filtered_targets) else "disabled")

    def target_button(self, target:Target, row):
        button = ttk.Button(
            row,
            text=f"{target.finnish_translations[0]}" if isinstance(target, Word)
            else f"{target.english_translations[0]}",
            style="Target.TButton",
            command=lambda: self.target_button_pressed(target))
        button.pack(side="left", padx=10)

    def change_page_by(self, amount:int):
        self.current_page += amount
        self.update_target_buttons()

    def on_search(self, event=None):
        query = self.search_var.get().lower()
        # If the user is on the word page:
        if self.showing == "word":
            self.filtered_targets = [
                word for word in self.available_words
                if query in word.finnish_translations[0].lower()
            ]
        # If the user is on the grammar page:
        elif self.showing == "grammar":
            self.filtered_targets = [
                grammar for grammar in self.available_grammar
                if query in grammar.english_translations[0].lower()
            ]
        self.current_page = 0
        self.update_target_buttons()

    def target_button_pressed(self, target):
        self.controller.current_lesson = target
        self.controller.show_frame("Lesson")

    def back(self):
        self.controller.show_frame("HomePage")