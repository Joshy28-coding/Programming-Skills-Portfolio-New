from tkinter import *
import json
from pathlib import Path
from PIL import Image, ImageTk

# ===================================
# What I've learned - Notes
# ====================================

# What is anchor exactly? -  controls alignment inside the space a widget has been given. 
# It’s different from side: side chooses which side of the parent the widget is placed on; anchor aligns it within its allotted space.
# With fill="x", there’s no extra horizontal space to align within.


# I've used UTF-8 to help encode text so computers can store and read characters.
# This will be useful later on when I implement the difficulties dictionary.
data_path = Path(__file__).parent / "resources" / "01-MathQuiz-Data.json"
with data_path.open('r', encoding="utf-8") as f:
    data = json.load(f)

COLORS = data["COLORS"]
# I've learned that tuple conversion from .json to .py helps me keep the font settings recognizable to the Tkinter code.
FONTS = {name: tuple(font) for name, font in data["FONTS"].items()}
DIFFICULTIES = data["DIFFICULTIES"]

# ====================================
# Application Root
# ====================================

root = Tk()
root.geometry("900x800")
root.title("Arithmetic Math Quiz")

root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.resizable(0, 0)

# ====================================
# Importing Data file
# ====================================

# sidebar_main = Frame(root, width=250, bg=COLORS["bg_card_inner"])
# sidebar_main.grid(row=0, column=0, sticky="ns")
# sidebar_main.pack_propagate(False)

container = Frame(root)
container.grid(row=0, column=1, sticky="nsew")
container.config(width=600, height=600)
pages = {}

current_difficulty = ""
current_question = 0
score = 0
attempts = 0
correct_answer = 0

# Load the background image for home_frame
bg_image_home = Image.open(Path(__file__).parent / "resources" / "mathquiz_bg.png")
bg_photo_home = ImageTk.PhotoImage(bg_image_home)

# - Loading the image buttons was prompted and assisted by A.I
easybtn = Image.open(Path(__file__).parent / "resources" / "easybtn.png")
easy_photo_btn = ImageTk.PhotoImage(easybtn.resize((240, 84)))

moderatebtn = Image.open(Path(__file__).parent / "resources" / "moderatebtn.png")
moderate_photo_btn = ImageTk.PhotoImage(moderatebtn.resize((240, 84)))

hardbtn = Image.open(Path(__file__).parent / "resources" / "hardbtn.png")
hard_photo_btn = ImageTk.PhotoImage(hardbtn.resize((240, 84)))

DIFFICULTY_BUTTON_IMAGES = {
    "easy": easy_photo_btn,
    "moderate": moderate_photo_btn,
    "advanced": hard_photo_btn,
}

def show_page(name):
    for page in pages.values():
        page.pack_forget()

    pages[name].pack(fill="both", expand=True)

'''I've decided to archive this function just in case I'd need it later, after further thought I've decided the options/sidebar on the left is bad U.I design. But just in case I'll keep it as comments for now'''
# def difficultysidebar():
#     sidebar = Frame(sidebar_main, bg=COLORS["bg_card_inner"])
#     sidebar.columnconfigure(0, weight=1)

#     difficultyhead = Label(
#         sidebar, text="Difficulty\nSelector",
#         fg=COLORS["fg_text"], bg=COLORS["bg_card_inner"],
#         font=FONTS["body_bold"],
#     )
#     difficultyhead.grid(row=0, column=0, sticky="ew", padx=10, pady=30)
    
#     easy_btn = Button(
#         sidebar, text="Easy",
#         fg=COLORS["fg_text"], bg=COLORS["bg_card"],
#         font=FONTS["body_bold"], height=2, relief = FLAT
#     )
#     easy_btn.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

#     moder_btn = Button(
#         sidebar, text="Moderate",
#         fg=COLORS["fg_text"], bg=COLORS["bg_card"],
#         font=FONTS["body_bold"], height=2, relief = FLAT
#     )
#     moder_btn.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

#     hard_btn = Button(
#         sidebar, text="Hard",
#         fg=COLORS["fg_text"], bg=COLORS["bg_card"],
#         font=FONTS["body_bold"], height=2, relief = FLAT
#     )
#     hard_btn.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

#     return sidebar

# sidebar = difficultysidebar()
# sidebar.pack(fill="both", expand=True)

def difficultycrd(parent, difficulty, details, column):
    
    title = difficulty.title()
    color = COLORS[difficulty]
    
    card = Frame(parent, bg=COLORS["bg_card"], height=350, width=270)
    card.grid(row=0, column=column, sticky="nsew", padx=8, pady=8)
    # the card’s contents use pack(). By default, pack lets those contents determine the card’s size, overriding the height i've set.
    # Propogate helps keep the card's set height instead of letting its packed contents resize it.
    card.pack_propagate(False)
    
    accent = Frame(card, bg=color, height=5)
    accent.pack(side=TOP, fill="x")
    
    content = Frame(card, bg=COLORS["bg_card"])
    content.pack(side=LEFT, expand=True, fill="both", padx=16, pady=12)
    
    Label(
        content,
        text=(
            f"{details['number_label']}\n"
            f"({details['min_number']} - {details['max_number']})\n"
            f"{details['question_count']} questions"
        ), font=FONTS["heading"], bg=COLORS["bg_card"], fg=COLORS["fg_text"], wraplength=240, 
    ).pack(anchor="w", fill="x", pady=8)

    Label(content, text=details["description"], font=("Helvetica", 10), bg=COLORS["bg_card"], fg=COLORS["fg_muted"], wraplength=240).pack(anchor="w", fill="x", pady=20)

    Button(
        content, image=DIFFICULTY_BUTTON_IMAGES[difficulty], command=lambda: show_page("quiz"), bg=COLORS["bg_card"], activebackground=COLORS["bg_card"],
        borderwidth=0, highlightthickness=0, relief=FLAT,
    ).pack(pady=(0, 40), side=BOTTOM)
    
    return card

def mainhomescreen(parent):
    frame = Frame(parent, bg=COLORS["bg_color"])
    background = Label(frame, image=bg_photo_home)
    background.place(x=0, y=0, relwidth=1, relheight=1)
    background.lower()
    
    Label(frame, text="- Arithmetic Math Quiz -", bg=COLORS["bg_color"], fg=COLORS["fg_text"], font=FONTS["title"]).pack(pady=(100, 10))
    Label(frame, text="Welcome to the Quiz!", bg=COLORS["bg_color"], fg=COLORS["fg_text"], font=("Courier New", 30, "bold")).pack()
    Label(frame, text="Choose your challenge tier. Each tier has 10 questions each.\n"
             "Earn 10 points on your first attempt, or 5 points on your second.",
        bg=COLORS["bg_color"], fg=COLORS["fg_muted"], font=FONTS["muted"], justify="center").pack(pady=(20, 20))
    
    cards = Frame(frame, bg=COLORS["bg_color"])
    cards.pack()

    # The first loop makes three equal-width card columns; the second creates one difficulty card per JSON entry and places it in its matching column.
    for column in range(3):
        cards.grid_columnconfigure(column, weight=1, uniform="difficulty")
    for column, (difficulty, details) in enumerate(DIFFICULTIES.items()):
        difficultycrd(cards, difficulty, details, column)

    return frame

def mainquizpage(parent):
    frame = Frame(parent)
    background = Label(frame, image=bg_photo_home)
    background.place(x=0, y=0, relwidth=1, relheight=1)
    background.lower()

    Button(frame, text="Back to home", command=lambda: show_page("home")).pack()

    return frame


pages["home"] = mainhomescreen(container)
pages["quiz"] = mainquizpage(container)

show_page("home")
root.mainloop()