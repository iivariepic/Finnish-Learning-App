# File name: app.py
# Author: Iivari Anttila
# Description: The main class for the tkinter app

import tkinter as tk
from tkinter import ttk
import datetime


from databaseHandler import DatabaseHandler
from targetTypes.phrase import Phrase
from GUI.styleConstants import setup_styles
from GUI.selectUser import SelectUser
from GUI.newUser import NewUser
from GUI.homePage import HomePage
from GUI.modifyUser import ModifyUser
from GUI.reviews import Reviews
from GUI.allLessons import AllLessons


class App(tk.Tk):
    ALL_FRAMES:list[ttk.Frame] = [
        SelectUser, NewUser, HomePage, ModifyUser, Reviews, AllLessons
    ]

    def __init__(self):
        super().__init__()
        self.current_user = None
        self.database = DatabaseHandler()
        self.title("Finnish Learning App")
        self.geometry("600x400")
        self.current_frame_name = ""

        # Make on_window_close run every time window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        setup_styles()

        self.frames = {}
        for frame in self.ALL_FRAMES:
            new_frame = frame(container, self)
            self.frames[frame.__name__] = new_frame
            new_frame.grid(row=0, column=0, sticky="nsew")
            container.rowconfigure(0, weight=1)
            container.columnconfigure(0, weight=1)

        self.show_frame(list(self.frames.keys())[0])

    def show_frame(self, page_name):
        self.current_frame_name = page_name
        frame = self.frames[page_name]
        # Update the user in the frame if needed
        update_user = getattr(frame, "update_user", None)
        if callable(update_user):
            frame.update_user()
        frame.tkraise()

    def on_window_close(self):
        if self.current_frame_name == "Reviews":
            frame = self.frames["Reviews"]
            frame.save_progress()

        self.destroy()

    def get_reviews(self):
        assert self.current_user is not None
        user = self.current_user
        result = []
        for learning_progress in user.learning_progresses:
            if learning_progress.due_date <= datetime.date.today():
                result.append(learning_progress)

        return result

    def get_unlearned_targets(self):
        assert self.current_user is not None
        user = self.current_user
        all_targets = self.database.get_not_learned_targets(user)
        # Phrases are not learnable targets
        return [
            target for target in all_targets if not isinstance(target, Phrase)
        ]

# Testing:
if __name__ == "__main__":
    app = App()
    app.mainloop()