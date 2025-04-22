# File name: styleConstants.py
# Author: Iivari Anttila
# Description: File to store constants of the style like font
from tkinter import ttk

CONTENT_FONT = ("Cooper Std Black", 12)
CONTENT_FONT_BOLD = ("Cooper Std Black", 12, "bold")
SUBHEADER_FONT = ("Cooper Std Black", 16)
HEADER_FONT = ("Cooper Std Black", 20, "bold")

CORRECT_COLOR = "#9DF298"
WRONG_COLOR = "#F67577"

LIGHT_BLUE = "#98E9F2"
BLUE = "#66CEDD"

def setup_styles():
    style = ttk.Style()
    style.configure("Custom.TButton", font=CONTENT_FONT, padding=10)
    style.configure("Arrow.TButton", font=CONTENT_FONT, padding=5)
    style.configure("Custom.TEntry", font=CONTENT_FONT, padding=2)
    style.configure("Custom.TLabel", font=CONTENT_FONT)
    style.configure("CustomBold.TLabel", font=CONTENT_FONT_BOLD)
    style.configure("ReviewCorrect.TLabel", font=CONTENT_FONT, background=CORRECT_COLOR)
    style.configure("ReviewWrong.TLabel", font=CONTENT_FONT, background=WRONG_COLOR)
    style.configure("LessonHeader.TLabel", font=HEADER_FONT, background=LIGHT_BLUE)
    style.configure("LessonSubHeader.TLabel", font=SUBHEADER_FONT, background=LIGHT_BLUE)
    style.configure("LessonHeader.TFrame", background=LIGHT_BLUE)
    style.configure("Target.TButton", font=CONTENT_FONT, padding=5, background=LIGHT_BLUE)
    style.map("Target.TButton", background=[('active', BLUE)])