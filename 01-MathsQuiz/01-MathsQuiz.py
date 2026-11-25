from tkinter import *
import json
from pathlib import Path
from PIL import Image, ImageTk
import random

# ===================================
# What I've learned - Notes
# ====================================

# What is anchor exactly? -  controls alignment inside the space a widget has been given. 
# It’s different from side: side chooses which side of the parent the widget is placed on; anchor aligns it within its allotted space.
# With fill="x", there’s no extra horizontal space to align within.

# What is Global? - tells Python that an assignment inside a function should update a variable defined outside it, rather than create a separate local variable.

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

# ============================================
# Main Functions
# ============================================

def mainquestionf():
    
    details=DIFFICULTIES[current_difficulty]
    first_number = random.randint(details["min_number"], details["max_number"])
    second_number = random.randint(details["min_number"], details["max_number"])
    operation = random.choice(("+", "-"))

    if operation == "+":
        correct_answer = first_number + second_number
    else:
        if second_number > first_number:
            first_number, second_number = second_number, first_number
        correct_answer = first_number - second_number
        
    question_label.config(text=f"{first_number} {operation} {second_number} = ?")
    progress_label.config(
        text=f"Question {current_question} of {details['question_count']}"
    )
    score_label.config(text=f"Score: {score}")
    feedback_label.config(text="")
    answer_entry.config(state=NORMAL)
    answer_entry.delete(0, END)
    submit_button.config(state=NORMAL)
    next_button.config(state=DISABLED)
    attempts = 0
    
def start_quiz(difficulty):
    global current_difficulty, current_question, score

    current_difficulty = difficulty
    current_question = 1
    score = 0
    next_button.config(text="Next question", command=nextquestionf)
    mainquestionf()
    show_page("quiz")
    answer_entry.focus_set()

def checkanswer():
    global attempts, score

    try:
        guess = int(answer_entry.get())
    except ValueError:
        feedback_label.config(text="Enter a whole number.", fg=COLORS["error"])
        return

    if guess == correct_answer:
        points = 10 if attempts == 0 else 5
        score += points
        score_label.config(text=f"Score: {score}")
        feedback_label.config(
            text=f"Correct! You earned {points} points.",
            fg=COLORS[current_difficulty],
        )
        answer_entry.config(state=DISABLED)
        submit_button.config(state=DISABLED)
        next_button.config(state=NORMAL)
    else:
        attempts += 1
        if attempts == 1:
            feedback_label.config(
                text="Not quite. Try one more time.",
                fg=COLORS["error"],
            )
        else:
            feedback_label.config(
                text=f"The answer was {correct_answer}.",
                fg=COLORS["error"],
            )
            answer_entry.config(state=DISABLED)
            submit_button.config(state=DISABLED)
            next_button.config(state=NORMAL)

# =============================================
# Front-end visuals / frame functions
# =============================================

def show_page(name):
    for page in pages.values():
        page.pack_forget()

    pages[name].pack(fill="both", expand=True)

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
    global question_label, progress_label, score_label, feedback_label
    global answer_entry, submit_button, next_button    

    frame = Frame(parent)
    background = Label(frame, image=bg_photo_home)
    background.place(x=0, y=0, relwidth=1, relheight=1)
    background.lower()

    Button(frame, text="Back to home", command=lambda: show_page("home"), bg=COLORS["bg_card"], fg=COLORS["fg_text"], relief=FLAT,).pack(anchor="w", padx=24, pady=20)
    
    quiz_card = Frame(frame, bg=COLORS["bg_card"])
    quiz_card.pack(fill="x", padx=150, pady=(70, 0))

    status_row = Frame(quiz_card, bg=COLORS["bg_card"])
    status_row.pack(fill="x", padx=24, pady=(20, 10))
    progress_label = Label(status_row, text="", font=FONTS["body"], bg=COLORS["bg_card"], fg=COLORS["fg_muted"],)
    progress_label.pack(side=LEFT)

    score_label = Label(status_row, text="Score: 0", font=FONTS["body_bold"], bg=COLORS["bg_card"],fg=COLORS["fg_text"],)
    score_label.pack(side=RIGHT)

    question_label = Label(quiz_card, text="Choose a difficulty to begin.", font=("Arial", 30, "bold"), bg=COLORS["bg_card"], fg=COLORS["fg_text"], wraplength=500,)
    question_label.pack(pady=(35, 20))

    answer_entry = Entry(quiz_card, font=FONTS["heading"], justify="center", bg=COLORS["bg_entry"], fg=COLORS["fg_text"], insertbackground=COLORS["fg_text"], relief=FLAT,)
    answer_entry.pack(padx=24, pady=10, ipadx=12, ipady=8)
    feedback_label = Label(quiz_card, text="", font=FONTS["body"], bg=COLORS["bg_card"], fg=COLORS["fg_muted"],)
    feedback_label.pack(pady=8)

    actions = Frame(quiz_card, bg=COLORS["bg_card"])
    actions.pack(pady=(12, 24))
    
    submit_button = Button(actions, text="Submit answer", command=checkanswerf, bg=COLORS["bg_card_inner"], fg=COLORS["fg_text"],relief=FLAT,)
    submit_button.pack(side=LEFT, padx=6)

    next_button = Button(actions, text="Next question", command=nextquestionf, state=DISABLED, bg=COLORS["bg_card_inner"], fg=COLORS["fg_text"], disabledforeground=COLORS["fg_muted"], relief=FLAT,)
    next_button.pack(side=LEFT, padx=6)
    return frame


pages["home"] = mainhomescreen(container)
pages["quiz"] = mainquizpage(container)

show_page("home")
root.mainloop()