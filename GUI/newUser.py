# File name: newUser.py
# Author: Iivari Anttila
# Description: Class for the GUI of creating a new user
from tkinter import ttk
import tkinter as tk
from GUI.styleConstants import *
from user import User

class NewUser(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)

        # Header
        header = ttk.Label(self, text="Create a New User", font=HEADER_FONT, anchor="center")
        header.grid(row=0, column=0, pady=20, sticky="ew")

        # User ID indicator
        self.next_id = self.controller.database.get_next_user_id()
        id_label = ttk.Label(self, text=f"User ID:")
        id_label.grid(row=1, column=0)
        id_value_label = ttk.Label(self, text=f"{self.next_id}")
        id_value_label.grid(row=1, column=1)

        # Username Entry
        entry_label = ttk.Label(self, text="Enter Username:")
        entry_label.grid(row=2, column=0)

        self.username = tk.StringVar()
        username_entry = ttk.Entry(self, textvariable=self.username, style="Custom.TEntry")
        username_entry.grid(row=2, column=1)
        username_entry.bind("<KeyRelease>", self.check_entry)

        # Submit Button
        self.button_submit = ttk.Button(
            self,
            text="Create User",
            state="disabled",
            style="User.TButton",
            command=lambda: self.submit
        )
        self.button_submit.grid(row=3, column=0, pady=30)

    def check_entry(self):
        entry = self.username.get()
        self.button_submit.config(state="normal" if 0 < len(entry) < 50 else "disabled")

    def submit(self):
        new_user = User(self.next_id, self.username.get())
        self.controller.database.new_user(new_user)
        self.controller.show_frame("SelectUser")