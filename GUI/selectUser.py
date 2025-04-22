# File name: selectUser.py
# Author: Iivari Anttila
# Description: Class for the GUI function to select a user
from GUI.styleConstants import *
import tkinter as tk
import math
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
        please_select = ttk.Label(self, text="Please Select A Profile", font=CONTENT_FONT, anchor="center")
        please_select.grid(row=1, column=0, pady=20, sticky="ew")

        # User buttons
        self.button_container = ttk.Frame(self)
        self.button_container.grid(row=2, column=0, pady=20, sticky="")

        # "Page" navigation buttons
        navigation_frame = ttk.Frame(self)
        navigation_frame.grid(row=3, column=0, pady=20)
        self.button_previous = ttk.Button(
            navigation_frame,
            text = "←",
            command=lambda: self.change_page_by(-1),
            style="Arrow.TButton"
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
            style="Arrow.TButton"
        )

        self.button_previous.pack(side="left", padx=10)
        self.button_middle_label.pack(side="left", padx=10)
        self.button_next.pack(side="left", padx=10)

        self.update_user_buttons()

        # Searching
        search_frame = ttk.Frame(self)
        search_frame.grid(row=4, column=0, pady=(0, 5), padx=20, sticky="ew")

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

    def user_button(self, user:User):
        first_name = user.first_name

        if len(first_name) > 8:
            first_name = first_name[:8] + "..."

        if self.check_matching_first_names(user):
            first_name += f" ({user.user_id})"

        button = ttk.Button(
            self.button_container,
            text=f"{first_name}",
            style="Custom.TButton",
            command=lambda: self.user_button_pressed(user))
        button.pack(side="left", padx=10)

    def create_user_button(self):
        button_create_user = ttk.Button(
            self.button_container,
            text="Create New",
            command=self.create_user_button_pressed,
            style="Custom.TButton"
        )
        button_create_user.pack(side="left", padx=10)

    def check_matching_first_names(self, user:User):
        for other_user in self.all_users:
            is_user = other_user == user
            same_name = other_user.first_name == user.first_name

            if not is_user and same_name:
                return True
        return False

    def update_user_buttons(self):
        # Clear the old buttons
        for widget in self.button_container.winfo_children():
            widget.destroy()

        start = self.current_page * self.USERS_PER_PAGE
        end = start + self.USERS_PER_PAGE
        page_users = self.filtered_users[start:end]

        for user in page_users:
            self.user_button(user)

        # Add a "Create User" button to the end of the list
        if len(page_users) < 4:
            self.create_user_button()

        # Disable navigation buttons at page boundaries
        self.button_previous.config(state="normal" if self.current_page > 0 else "disabled")
        self.button_middle_label.config(
            text=f"{self.current_page + 1}/{math.ceil((len(self.filtered_users) + 1)/self.USERS_PER_PAGE)}"
        )
        self.button_next.config(state="normal" if end < len(self.filtered_users) + 1 else "disabled")

        # Set the label to 1 if there are no users
        if len(self.filtered_users) == 0:
            self.button_middle_label.config(
                text=f"1/1"
            )

    def change_page_by(self, amount:int):
        self.current_page += amount
        self.update_user_buttons()

    def user_button_pressed(self, user:User):
        self.controller.current_user = user
        self.controller.show_frame("HomePage")

    def on_search(self, event=None):
        query = self.search_var.get().lower()
        self.filtered_users = [user for user in self.all_users if query in user.first_name.lower()]
        self.current_page = 0
        self.update_user_buttons()

    def create_user_button_pressed(self):
        self.controller.show_frame("NewUser")

    def update_user(self):
        self.search_var.set("")
        self.all_users = self.controller.database.form_all_users()
        self.filtered_users = self.all_users
        self.current_page = 0
        self.update_user_buttons()