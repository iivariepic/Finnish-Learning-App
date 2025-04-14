# File name: styleConstants.py
# Author: Iivari Anttila
# Description: File to store constants of the style like font
from tkinter import ttk


CONTENT_FONT = ("Cooper Std Black", 12)
HEADER_FONT = ("Cooper Black", 20)

CORRECT_COLOR = "#9DF298"
WRONG_COLOR = "#F67577"

def setup_styles():
    style = ttk.Style()
    style.configure("Custom.TButton", font=CONTENT_FONT, padding=10)
    style.configure("Custom.TEntry", font=CONTENT_FONT, padding=2)
    style.configure("Custom.TLabel", font=CONTENT_FONT)
    style.configure("ReviewCorrect.TLabel", font=CONTENT_FONT, background=CORRECT_COLOR)
    style.configure("ReviewWrong.TLabel", font=CONTENT_FONT, background=WRONG_COLOR)