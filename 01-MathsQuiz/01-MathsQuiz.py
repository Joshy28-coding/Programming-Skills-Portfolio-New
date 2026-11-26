from tkinter import *
import json
from pathlib import Path
from PIL import Image, ImageTk
import random

# ==================================================
# Math Quiz Overview
# ==================================================
#  01 - MathQuiz, submitted by Josh Louis R. Contreras Creative Computing Level 5.
#  This quiz covers the necessary requirements expected for this quiz.
#   - Develop a GUI Tkinter application that functions as a MathQuiz.
#   - The main screen is presented with a short menu of difficulty options to select.
#   - Difficulty determines the number of digits to be added or subtracted. Easy(singe digits), Moderate(double digits), Advanced(4-digits).
#   - When the user submits the correct answer on the first attempt they get 10 pts, if second 5 pts. If they fail the second, they fail the question and move on to the next question.
#   - Small widgets such as score count and question progress is displayed during the quiz.
#   - The question's values are scrambled for addition and subtraction operations, they use the random module.
#   - !!! What code you see here is mostly taken and learned from the 'Advanced Python' materials given to us as reference.
#   - !!! the '01-MathQuiz-Data-json' file contains dict. for Colors, fonts, difficulty items and rankings.

#   - I acknowledge I have used A.I to assist me in bug-testing and SOME implementation complex functions such as Rankings functions and implementing buttons.

# ===================================
# What I've learned - Notes
# ====================================

# What is anchor exactly? -  controls alignment inside the space a widget has been given. 
# It’s different from side: side chooses which side of the parent the widget is placed on; anchor aligns it within its allotted space.
# With fill="x", there’s no extra horizontal space to align within.

# What is Global? - tells Python that an assignment inside a function should update a variable defined outside it,
# rather than create a separate local variable.

# I've used UTF-8 to help encode text so computers can store and read characters.
# This will be useful later on when I implement the difficulties dictionary.
data_path = Path(__file__).parent / "resources" / "01-MathQuiz-Data.json"
with data_path.open('r', encoding="utf-8") as f:
    data = json.load(f)

COLORS = data["COLORS"]
# I've learned that tuple conversion from .json to .py helps me keep the font settings recognizable to the Tkinter code.
FONTS = {name: tuple(font) for name, font in data["FONTS"].items()}
DIFFICULTIES = data["DIFFICULTIES"]
RANKINGS = data["RANKINGS"]

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
    global attempts, correct_answer
    
    details=DIFFICULTIES[current_difficulty]
    
    # Generate two random numbers based on the selected difficulty
    first_number = random.randint(details["min_number"], details["max_number"])
    second_number = random.randint(details["min_number"], details["max_number"])
    operation = random.choice(("+", "-"))

    # Randomly choose addition or subtraction.
    if operation == "+":
        correct_answer = first_number + second_number
    else:
        # Swap the numbers if needed to avoid a negative answer.
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

def startquizf(difficulty):
    global current_difficulty, current_question, score

    current_difficulty = difficulty
    current_question = 1
    score = 0
    next_button.config(text="Next question", command=nextquestionf)
    mainquestionf()
    show_page("quiz")
    answer_entry.focus_set()

def checkanswerf():
    global attempts, score

    # Check if the answer is a valid whole number
    try:
        guess = int(answer_entry.get())
        
    except ValueError:
        feedback_label.config(text="Enter a whole number.", fg=COLORS["error"])
        return

    # Check whether the answer is correct
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
                text="Not quite.\nTry one more time.",
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

def nextquestionf():
    global current_question

    question_count = DIFFICULTIES[current_difficulty]["question_count"]
    if current_question == question_count:
        maximum_score = question_count * 10
        rank, rank_description = calculaterankf()
        result_title_label.config(text=f"{current_difficulty.title()} quiz complete!")
        result_score_label.config(
            text=f"Final score: {score} / {maximum_score}")
        result_rank_label.config(text=f"Rank: {rank}")
        result_description_label.config(text=rank_description)
        show_page("results")
        return

    current_question += 1
    mainquestionf()  

# - This function has been generated by A.I after implementing the RANKINGS in .json file
def calculaterankf():
    question_count = DIFFICULTIES[current_difficulty]["question_count"]
    # Use a percentage so rank thresholds work even if quiz lengths change.
    score_percentage = score / (question_count * 10) * 100
    # Check the highest threshold first to return the best qualifying rank.
    for rank, details in sorted(
        RANKINGS.items(),
        key=lambda ranking: ranking[1]["minimum"],
        reverse=True):
        if score_percentage >= details["minimum"]:
            return rank, details["description"]
    raise ValueError("No ranking threshold matches the final score.")


# =============================================
# Front-end visuals / GUI Functions
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

    Button(content, command=lambda level=difficulty: startquizf(level), bg=COLORS["bg_card"], image=DIFFICULTY_BUTTON_IMAGES[difficulty], activebackground=COLORS["bg_card"],
        borderwidth=0, highlightthickness=0, relief=FLAT
    ).pack(pady=(0, 70), side=BOTTOM)
    
    return card

def mainhomescreen(parent):
    frame = Frame(parent, bg=COLORS["bg_color"])
    background = Label(frame, image=bg_photo_home)
    background.place(x=0, y=0, relwidth=1, relheight=1)
    background.lower()
    
    Label(frame, text="- Arithmetic Math Quiz -", bg=COLORS["bg_color"], fg=COLORS["moderate"], font=FONTS["title"]).pack(pady=(100, 10))
    Label(frame, text="Welcome to the Quiz!", bg=COLORS["bg_color"], fg=COLORS["fg_text"], font=("Courier New", 30, "bold")).pack()
    Label(frame, text="Choose your challenge tier. Each tier has 10 questions each.\n"
             "Earn 10 points on your first attempt, or 5 points on your second.",
        bg=COLORS["bg_color"], fg=COLORS["fg_muted"], font=FONTS["muted"], justify="center").pack(pady=(20, 20))
    
    cards = Frame(frame, bg=COLORS["bg_color"])
    cards.pack()

    # Make the three difficulty cards in equal width.
    for column in range(3):
        cards.grid_columnconfigure(column, weight=1, uniform="difficulty")
    
    # Add each difficulty card from the JSON data.
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

    Button(frame, text="Back to home", command=lambda: show_page("home"), font=FONTS["body_bold"], bg=COLORS["bg_card"], fg=COLORS["fg_text"], relief=FLAT, width=12, height=2).pack(anchor="w", padx=24, pady=20)
    
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

    answer_entry = Entry(quiz_card, justify="center", bg=COLORS["bg_entry"], font=FONTS["body_bold"], fg=COLORS["fg_text"], insertbackground=COLORS["fg_text"], relief=FLAT,)
    answer_entry.pack(padx=24, pady=10, ipadx=12, ipady=8)
    feedback_label = Label(quiz_card, text="", font=FONTS["body"], bg=COLORS["bg_card"], fg=COLORS["fg_muted"],)
    feedback_label.pack(pady=8)

    actions = Frame(quiz_card, bg=COLORS["bg_card"])
    actions.pack(pady=(12, 24))
    
    submit_button = Button(actions, text="Submit answer", command=checkanswerf, font=FONTS["body_bold"], bg=COLORS["bg_card_inner"], fg=COLORS["fg_text"],relief=FLAT, width=15, height=3)
    submit_button.pack(side=LEFT, padx=6)

    next_button = Button(actions, text="Next question", command=nextquestionf, font=FONTS["body_bold"], state=DISABLED, bg=COLORS["bg_card_inner"], fg=COLORS["fg_text"], disabledforeground=COLORS["fg_muted"], relief=FLAT, width=15, height=3)
    next_button.pack(side=LEFT, padx=6)
    
    return frame

def mainresultspage(parent):
    global result_title_label, result_score_label
    global result_rank_label, result_description_label

    frame = Frame(parent)
    background = Label(frame, image=bg_photo_home)
    background.place(x=0, y=0, relwidth=1, relheight=1)
    background.lower()
    
    Button(frame, text="Back to home", command=lambda: show_page("home"), font=FONTS["body_bold"], bg=COLORS["bg_card"], fg=COLORS["fg_text"], relief=FLAT, width=15, height=3).pack(anchor="w", padx=24, pady=20)
    
    results_card = Frame(frame, bg=COLORS["bg_card"])
    results_card.pack(fill="x", padx=150, pady=(70, 10))

    result_title_label = Label(
    results_card, text="Quiz complete!", font=("Courier New", 30, "bold"), bg=COLORS["bg_card"], fg=COLORS["fg_text"])
    result_title_label.pack(pady=(30, 12))

    result_score_label = Label(results_card, text="", font=FONTS["body_bold"], bg=COLORS["bg_card"], fg=COLORS["fg_text"])
    result_score_label.pack(pady=(0, 30))

    result_rank_label = Label(results_card, text="", font=("Courier New", 30, "bold"), bg=COLORS["bg_card"], fg=COLORS["easy"])
    result_rank_label.pack(pady=(0, 8))

    result_description_label = Label(results_card, text="", font=FONTS["body"], bg=COLORS["bg_card"], fg=COLORS["fg_muted"])
    result_description_label.pack(pady=(0, 30))
    
    return frame


pages["home"] = mainhomescreen(container)
pages["quiz"] = mainquizpage(container)
pages["results"] = mainresultspage(container)


show_page("home")
root.mainloop()