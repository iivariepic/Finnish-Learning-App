# File name: app.py
# Author: Iivari Anttila
# Description: The main class for the tkinter app

import tkinter as tk
from tkinter import ttk


from databaseHandler import DatabaseHandler
from GUI.styleConstants import setup_styles
from GUI.selectUser import SelectUser
from GUI.newUser import NewUser
from GUI.homePage import HomePage

class App(tk.Tk):
    ALL_FRAMES:list[ttk.Frame] = [SelectUser, NewUser, HomePage]

    def __init__(self):
        super().__init__()
        self.current_user = None
        self.database = DatabaseHandler()
        self.title("Finnish Learning App")
        self.geometry("600x400")

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
        frame = self.frames[page_name]
        frame.tkraise()


# Testing:
if __name__ == "__main__":
    app = App()
    app.mainloop()