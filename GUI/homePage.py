# File name: homePage.py
# Author: Iivari Anttila
# Description: Class for the GUI of the Home Page (needs an user to be selected)
from GUI.styleConstants import *
import tkinter as tk
from tkinter import ttk
from user import User
import datetime

class HomePage(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user = None

        # Header
        self.columnconfigure(0, weight=1)
        self.header = ttk.Label(self, text="Welcome,", font=HEADER_FONT, anchor="center")
        self.header.grid(row=0, column=0, pady=20, sticky="ew")

        # Button frames
        upper_button_frame = ttk.Frame(self)
        upper_button_frame.grid(row=2, column=0, pady=20)

        lower_button_frame = ttk.Frame(self)
        lower_button_frame.grid(row=3, column=0, pady=20)

        # Lessons-button
        lessons_button = ttk.Button(
            upper_button_frame,
            text="Lessons",
            style="Custom.TButton",
            command=self.lessons_button_pressed
        )
        lessons_button.pack(side="left", padx=10)

        # Reviews-button
        reviews_button = ttk.Button(
            upper_button_frame,
            text="Reviews",
            style="Custom.TButton",
            command=self.reviews_button_pressed
        )
        reviews_button.pack(side="left", padx=10)

        # Review Amount indicator
        self.review_amount = ttk.Label(self, text="Reviews Due:", font=CONTENT_FONT, anchor="center")
        self.review_amount.grid(row=1, column=0, pady=(0,20))

        # Modify User-button
        modify_button = ttk.Button(
            lower_button_frame,
            text="Modify User Info",
            style="Custom.TButton",
            command=self.modify_button_pressed
        )
        modify_button.pack(side="left", padx=10)

        # Back-button
        back_button = ttk.Button(
            lower_button_frame,
            text="Back",
            style="Custom.TButton",
            command=self.back_button_pressed
        )
        back_button.pack(side="left", padx=10)


    def update_user(self):
        self.user = self.controller.current_user
        self.header.config(text=f"Welcome, {self.user.first_name}")
        self.update_review_amount()

    def update_review_amount(self):
        print("Updating Review Amount")

    def lessons_button_pressed(self):
        print("Going to Lessons")

    def reviews_button_pressed(self):
        print("Going to Reviews")

    def modify_button_pressed(self):
        # Refresh the select user page
        modify_page = self.controller.frames["ModifyUser"]
        modify_page.update_user()

        self.controller.show_frame("ModifyUser")

    def back_button_pressed(self):
        self.controller.current_user = None

        # Refresh the select user page
        select_page = self.controller.frames["SelectUser"]
        select_page.refresh_users()

        self.controller.show_frame("SelectUser")