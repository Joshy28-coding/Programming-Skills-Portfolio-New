from tkinter import *
import random
from pathlib import Path
from PIL import Image, ImageTk

# ===================================================================
# Joke Teller Application
# ===================================================================
# 02 - AlexaTellMeaJoke, submitted by Josh Louis R. Contreras Creative Computing Level 5.
# This quiz covers the expected requirements for this exercise
# - Background and buttons assets are designed and created in Canva.
# - The main screen features two buttons with their respective features. "Tell me a joke" and "Reveal Punchline"
# - Quit button functions as expected and closes/shuts down the program.
#   - !!! What code you see here is mostly taken and learned from the 'Advanced Python' materials given to us as reference.
#   - !!! the '01-MathQuiz-Data-json' file contains dict. for Colors, fonts, difficulty items and rankings.

#  - Most of the code you see here are written, learned and referenced from 'Python GUI lecture notes' materials provided by BathSpa RAK.

BASE_DIR = Path(__file__).resolve().parent
# Locate the resources folder and its text file.
JOKE_FILE = BASE_DIR / "resources" / "randomJokes.txt"

FONTS = {
    "joke": ["Arial", 17],
    "punchline": ["Arial", 19, "bold"]
}

# ====================================
# Application Root
# ====================================

root = Tk()
root.geometry("800x600")
root.title("Joke Teller - Haha")
root.resizable(0, 0)

bg_joke_teller = Image.open(Path(__file__).parent / "resources" / "bg_joke_teller.png")
bg_joke_photo = ImageTk.PhotoImage(bg_joke_teller)

with Image.open(BASE_DIR / "resources" / "quit_button.png") as quit_button_image:
    quit_button_photo = ImageTk.PhotoImage(quit_button_image.resize((48, 48)))

realframe = Frame(root)
realframe.pack(fill="both", expand=True)
pages = {}
current_joke = None

# Keeps selected pages in front.
def showpagef(name):
    for page in pages.values():
        page.pack_forget()

    pages[name].pack(fill="both", expand=True)

# Kept in mind on how to resize images from exercise 1 MathQuiz.
def loadbuttonimagesf(filename):
    with Image.open(BASE_DIR / "resources" / filename) as image:
        return ImageTk.PhotoImage(image.resize((210, 60)))

BUTTON_IMAGES = {
    "tell": loadbuttonimagesf("tell_joke.png"),
    "reveal": loadbuttonimagesf("reveal_punchline.png"),
    "next": loadbuttonimagesf("next_joke.png"),
}

def loadfunnyjokesf():
    jokes = []
    # Reads line by line of what's in the .txt file.
    try:
        with open(JOKE_FILE, "r", encoding="utf-8") as file_handler:
            for line in file_handler:
                line = line.strip()
            
                if not line:
                    continue
                
                # Identifies where to split the joke from the punchline. (?)
                setup, seperator, punchline = line.partition("?")
            
                if not seperator:
                    print(f"Skipping invalid joke: {line}")
                    continue
                
                # Adds / categorizes the data in the dataset.
                jokes.append({
                    "setup" : setup + seperator,
                    "punchline" : punchline.strip()
                })
        # Joke check in terminal
        print(f"Successfully loaded {len(jokes)} jokes.")
    
    except FileNotFoundError:
        print(f"Error: Could not find the joke file at {JOKE_FILE}")
    
    return jokes

jokelistf = loadfunnyjokesf()

def choosejokef():
    global current_joke

    if not jokelistf:
        joke_label.config(text="No jokes are available.")
        return
    
    available_jokes = [joke for joke in jokelistf if joke is not current_joke]
    # takes a random line of the already appended joke list.
    current_joke = random.choice(available_jokes or jokelistf)
    joke_label.config(text=current_joke["setup"])
    punchline_label.config(text="")
    tell_button.config(image=BUTTON_IMAGES["next"])
    reveal_button.config(state=NORMAL)

def revealpunchlinef():
    if current_joke is not None:
        punchline_label.config(text=current_joke["punchline"])

# ==========================================
# Frame Functions / Widgets
# ==========================================

def mainjokepage(parent):
    global joke_label, punchline_label, tell_button, reveal_button

    frame = Frame(parent)
    background = Label(frame, image=bg_joke_photo)
    background.place(x=0, y=0, relwidth=1, relheight=1)
    background.lower()

    quit_button = Button(frame, image=quit_button_photo, command=root.destroy, bg="#FFFFFF", activebackground="#FFFFFF", borderwidth=0, relief=FLAT)
    quit_button.place(relx=0.95, rely=0.065, anchor="ne")

    back_frames = Frame(frame, bg="#FFFFFF", bd=0, )
    back_frames.place(relx=0.5, rely=0.67, anchor="center")

    spacing = Frame(back_frames, width=465, height=200, bg="#FFFFFF", bd=0, )
    spacing.pack_propagate(False)
    spacing.pack()

    joke_label = Label(spacing, text="Click 'Tell me a joke' to begin!", font=FONTS["joke"], fg="#000000", bg="#FFFFFF", justify="center", wraplength=440)
    joke_label.pack(expand=True, fill="both", padx=12)
    punchline_label = Label(spacing, text="", fg="#E47812", font=FONTS["punchline"], bg="#FFFFFF", justify="center", wraplength=440)
    punchline_label.pack(expand=True, fill="both", padx=12)

    spacing1 = Frame(back_frames, width=465, height=100, bg="#FFFFFF", bd=0,)
    spacing1.pack_propagate(False)
    spacing1.pack(pady=(12, 0))
    tell_button = Button(spacing1, image=BUTTON_IMAGES["tell"], command=choosejokef, bg="#FFFFFF", activebackground="#FFFFFF", borderwidth=0, relief=FLAT)
    tell_button.pack(side=LEFT, padx=8, expand=True)
    reveal_button = Button(spacing1, image=BUTTON_IMAGES["reveal"], command=revealpunchlinef, state=DISABLED, bg="#FFFFFF", activebackground="#FFFFFF", disabledforeground="#080808", borderwidth=0, relief=FLAT,)
    reveal_button.pack(side=LEFT, padx=8, expand=True)
    return frame

pages["home"] = mainjokepage(realframe)

showpagef("home")
root.mainloop()