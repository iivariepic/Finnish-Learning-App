# File name: modifyUser.py
# Author: Iivari Anttila
# Description: Class for the GUI of modifying user information
from tkinter import ttk
import tkinter as tk
from GUI.styleConstants import *
from user import User

class ModifyUser(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)

        # Header
        self.header = ttk.Label(self, text="Modify User: ", font=HEADER_FONT, anchor="center")
        self.header.grid(row=0, column=0, columnspan=2, pady=(30, 20), sticky="ew")

        # User ID frame
        user_id_frame = ttk.Frame(self)
        user_id_frame.grid(row=1, column=0, pady=20)

        # User ID indicator
        id_label = ttk.Label(user_id_frame, text=f"User ID:", font=CONTENT_FONT)
        id_label.pack(side="left", padx=20)

        self.id:int = 0
        self.id_value_label = ttk.Label(user_id_frame, text=f"{self.id}", font=CONTENT_FONT)
        self.id_value_label.pack(side="left", padx=20)

        # Old first name frame
        old_name_frame = ttk.Frame(self)
        old_name_frame.grid(row=2, column=0, pady=20)

        # Old first name indicator
        name_label = ttk.Label(old_name_frame, text=f"Current First Name:", font=CONTENT_FONT)
        name_label.pack(side="left", padx=5)

        self.name_value_label = ttk.Label(old_name_frame, text="", font=CONTENT_FONT)
        self.name_value_label.pack(side="left", padx=5)

        # New first name frame
        new_name_frame = ttk.Frame(self)
        new_name_frame.grid(row=3, column=0, pady=20)

        # First Name Entry
        entry_label = ttk.Label(new_name_frame, text="New First Name:", font=CONTENT_FONT)
        entry_label.pack(side="left", padx=20)

        self.username = tk.StringVar()
        username_entry = ttk.Entry(new_name_frame, textvariable=self.username, style="Custom.TEntry")
        username_entry.pack(side="left", padx=20)
        username_entry.bind("<KeyRelease>", self.check_entry)

        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.grid(row=4, column=0, pady=20)

        # Back button
        back_button = ttk.Button(
            button_frame,
            text="Back",
            style="Custom.TButton",
            command=self.back
        )
        back_button.pack(side="left", padx=10)

        # Delete User Button
        delete_user_button = ttk.Button(
            button_frame,
            text="Delete User",
            style="Custom.TButton",
            command=self.delete_user
        )
        delete_user_button.pack(side="left", padx=10)

        # Change Name Button
        self.change_name_button = ttk.Button(
            button_frame,
            text="Change Name",
            state="disabled",
            style="Custom.TButton",
            command=self.change_name
        )
        self.change_name_button.pack(side="left", padx=10)

    def check_entry(self, event=None):
        entry = self.username.get()
        self.change_name_button.config(state="normal" if 0 < len(entry) < 50 else "disabled")
        self.change_name_button.config(
            state="disabled" if self.controller.current_user.first_name == entry else "normal"
        )

    def change_name(self):
        changed_user = User(self.id, self.username.get())
        self.controller.database.change_user(changed_user)

        self.username.set("")

        # Update the selected user
        self.controller.current_user = changed_user

        # Update the homepage
        home_page = self.controller.frames["HomePage"]
        home_page.update_user()

        self.controller.show_frame("HomePage")

    def update_user(self):
        user = self.controller.current_user

        self.name_value_label.config(text=f"{user.first_name}")
        self.id = user.user_id
        self.id_value_label.config(text=f"{self.id}")

    def delete_user(self):
        self.controller.database.delete_user(self.controller.current_user)
        self.controller.current_user = None

        # Refresh the select user page
        select_page = self.controller.frames["SelectUser"]
        select_page.update_user()

        self.controller.show_frame("SelectUser")

    def back(self):
        self.username.set("")
        self.controller.show_frame("HomePage")