# File name: styleConstants.py
# Author: Iivari Anttila
# Description: File to store constants of the style like font
from tkinter import ttk


CONTENT_FONT = ("Cooper Std Black", 12)
HEADER_FONT = ("Cooper Black", 20)

def setup_styles():
    style = ttk.Style()
    style.configure("User.TButton", font=CONTENT_FONT, padding=10)