from tkinter import *
import json
from pathlib import Path

# I've used UTF-8 to help encode text so computers can store and read characters.
# This will be useful later on when I implement the difficulties dictionary.
data_path = Path(__file__).parent / "resources" / "01-MathQuiz-Data.json"
with data_path.open('r', encoding="utf-8") as f:
    data = json.load(f)

COLORS = data["COLORS"]
# I've learned that tuple conversion from .json to .py helps me keep the font settings recognizable to the Tkinter code.
FONTS = {name: tuple(font) for name, font in data["FONTS"].items()}

# ====================================
# Application Root
# ====================================

root = Tk()
root.geometry("900x600")
root.title("Arithmetic Math Quiz")

root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# ====================================
# Importing Data file
# ====================================

sidebar_main = Frame(root, width=250, bg=COLORS["bg_card_inner"])
sidebar_main.grid(row=0, column=0, sticky="ns")
sidebar_main.pack_propagate(False)

container = Frame(root)
container.grid(row=0, column=1, sticky="nsew")
container.config(width=600, height=600)
pages = {}

def show_page(name):
    for page in pages.values():
        page.pack_forget()

    pages[name].pack(fill="both", expand=True)

#wdasdas
#adad
#adwdqwd
#dasdas
#dasdsad

def difficultysidebar():
    sidebar = Frame(sidebar_main, bg=COLORS["bg_card_inner"])
    sidebar.columnconfigure(0, weight=1)

    difficultyhead = Label(
        sidebar, text="Difficulty\nSelector",
        fg=COLORS["fg_text"], bg=COLORS["bg_card_inner"],
        font=FONTS["body_bold"],
    )
    difficultyhead.grid(row=0, column=0, sticky="ew", padx=10, pady=30)
    
    easy_btn = Button(
        sidebar, text="Easy",
        fg=COLORS["fg_text"], bg=COLORS["bg_card"],
        font=FONTS["body_bold"], height=2, relief = FLAT
    )
    easy_btn.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    moder_btn = Button(
        sidebar, text="Moderate",
        fg=COLORS["fg_text"], bg=COLORS["bg_card"],
        font=FONTS["body_bold"], height=2, relief = FLAT
    )
    moder_btn.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

    hard_btn = Button(
        sidebar, text="Hard",
        fg=COLORS["fg_text"], bg=COLORS["bg_card"],
        font=FONTS["body_bold"], height=2, relief = FLAT
    )
    hard_btn.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

    return sidebar

sidebar = difficultysidebar()
sidebar.pack(fill="both", expand=True)

def difficultycrd(parent, difficulty, details):
    
    card = Frame(parent, bg=COLORS["bg_card_inner"], height=250, width=300)
    card.pack(expand=True, padx=10, pady=10, anchor="w")
    
    content = Frame(card, bg=COLORS["bg_card_inner"])
    content.pack(side=LEFT, fill="both", expand=True, padx=16, pady=12)
    
    Label(
        content,
        text=(
            f"{details['number_label']} "
            f"({details['min_number']} – {details['max_number']}) · "
            f"{details['question_count']} questions"
        ),
        font=FONTS["body"], bg=COLORS["bg_card_inner"], fg=COLORS["fg_text"]
    ).pack(anchor="w", pady=3)

    Label(content, text=details["description"], font=("Helvetica", 10), bg=COLORS["bg_card_inner"], fg=COLORS["fg_muted"]).pack(anchor="w")
    
    return card

def mainhomescreen(parent):
    frame = Frame(parent, bg=COLORS["bg_color"])
    Label(frame, text="Arithmetic Math Quiz", bg=COLORS["bg_color"], fg=COLORS["fg_text"], font=FONTS["title"]).pack(pady=(150, 10))
    Label(frame, text="Welcome to the Quiz!", bg=COLORS["bg_color"], fg=COLORS["fg_text"], font=("Courier New", 26, "bold")).pack(pady=10)
    Label(frame, text="Choose your challenge tier. Each tier has 10 questions each.\n"
             "Earn 10 points on your first attempt, or 5 points on your second.",
        bg=COLORS["bg_color"], fg=COLORS["fg_text"], font=FONTS["muted"], justify="center").pack(pady=10)
    
    return frame

def mainquizpage(parent):
    frame = Frame(parent, bg="#1F2937")
    Label(frame, text="Question 1: What is 2 + 2?", bg="#1F2937", fg="white").pack(pady=20)
    Button(frame, text="Back to home", command=lambda: show_page("home")).pack()

    return frame


pages["home"] = mainhomescreen(container)
pages["quiz"] = mainquizpage(container)

show_page("home")
root.mainloop()