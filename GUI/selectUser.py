# File name: selectUser.py
# Author: Iivari Anttila
# Description: Class for the GUI function to select a user
from GUI.styleConstants import *
import tkinter as tk
from tkinter import ttk
from user import User

class SelectUser(ttk.Frame):
    USERS_PER_PAGE = 4

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.all_users = self.controller.database.form_all_users()
        self.filtered_users = self.all_users
        self.current_page = 0

        self.columnconfigure(0, weight=1)

        # Header of the page
        title = ttk.Label(self, text="Finnish Learning App", font=HEADER_FONT, anchor="center")
        title.grid(row=0, column=0, pady=20, sticky="ew")

        # "Please select a user"-text
        please_select = ttk.Label(self, text="Please Select A User", font=CONTENT_FONT, anchor="center")
        please_select.grid(row=1, column=0, pady=20, sticky="ew")

        # User buttons
        self.button_container = ttk.Frame(self)
        self.button_container.grid(row=2, column=0, pady=10)

        # "Page" navigation buttons
        navigation_frame = ttk.Frame(self)
        navigation_frame.grid(row=3, column=0, pady=10)
        self.button_previous = ttk.Button(
            navigation_frame,
            text = "←",
            command=lambda: self.change_page_by(-1),
            style="User.TButton"
        )

        self.button_middle_label = ttk.Label(
            navigation_frame,
            text=f"{self.current_page + 1}/{len(self.filtered_users)//5 + 1}",
            font=CONTENT_FONT
        )

        self.button_next = ttk.Button(
            navigation_frame,
            text = "→",
            command=lambda: self.change_page_by(1),
            style="User.TButton"
        )

        self.button_previous.pack(side="left", padx=10)
        self.button_middle_label.pack(side="left", padx=10)
        self.button_next.pack(side="left", padx=10)

        self.update_user_buttons()

        # Searching
        search_frame = ttk.Frame(self)
        search_frame.grid(row=4, column=0, pady=10)

        search_label = ttk.Label(search_frame, text="Search for Username:", font=CONTENT_FONT)
        search_label.pack()

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, style="Custom.TEntry")
        search_entry.pack()
        search_entry.bind("<KeyRelease>", self.on_search)

        # Create user-button
        button_create_user = ttk.Button(
            self,
            text="Create User",
            command=lambda: self.create_user_button_pressed(),
            style="User.TButton"
        )
        button_create_user.grid(row=5, pady=10)


    def create_user_button(self, user:User):
        button = ttk.Button(
            self.button_container,
            text=f"{user.first_name}",
            style="User.TButton",
            command=lambda: self.user_button_pressed(user))
        button.pack(side="left", padx=10)

    def update_user_buttons(self):
        # Clear the old buttons
        for widget in self.button_container.winfo_children():
            widget.destroy()

        start = self.current_page * self.USERS_PER_PAGE
        end = start + self.USERS_PER_PAGE
        page_users = self.filtered_users[start:end]

        for user in page_users:
            self.create_user_button(user)

        # Disable navigation buttons at page boundaries
        self.button_previous.config(state="normal" if self.current_page > 0 else "disabled")
        self.button_middle_label.config(
            text=f"{self.current_page + 1}/{len(self.filtered_users)//self.USERS_PER_PAGE + 1}"
        )
        self.button_next.config(state="normal" if end < len(self.filtered_users) else "disabled")

    def change_page_by(self, amount:int):
        self.current_page += amount
        self.update_user_buttons()

    def user_button_pressed(self, user:User):
        self.controller.current_user = user
        print(f"User selected: {self.controller.current_user.first_name}")
        return

    def on_search(self, event=None):
        query = self.search_var.get().lower()
        self.filtered_users = [user for user in self.all_users if query in user.first_name.lower()]
        self.current_page = 0
        self.update_user_buttons()

    def create_user_button_pressed(self):
        self.controller.show_frame("NewUser")

    def refresh_users(self):
        self.all_users = self.controller.database.form_all_users()
        self.filtered_users = self.all_users
        self.current_page = 0
        self.update_user_buttons()