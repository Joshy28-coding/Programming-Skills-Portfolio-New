from tkinter import *
import random
from pathlib import Path
from PIL import Image, ImageTk

BASE_DIR = Path(__file__).resolve().parent
# Locate the resources folder and its text file.
JOKE_FILE = BASE_DIR / "resources" / "randomJokes.txt"

root = Tk()
root.geometry("800x600")
root.title("Joke Teller - Haha")
root.resizable(0, 0)

bg_joke_teller = Image.open(Path(__file__).parent / "resources" / "bg_joke_teller.png")
bg_joke_photo = ImageTk.PhotoImage(bg_joke_teller)

realframe = Frame(root)
realframe.pack(fill="both", expand=True)
pages = {}

def showpagef(name):
    for page in pages.values():
        page.pack_forget()

    pages[name].pack(fill="both", expand=True)

def loadfunnyjokesf():
    jokes = []
    
    try:
        with open(JOKE_FILE, "r", encoding="utf-8") as file_handler:
            for line in file_handler:
                line = line.strip()
            
                if not line:
                    continue
            
                setup, seperator, punchline = line.partition("?")
            
                if not seperator:
                    print(f"Skipping invalid joke: {line}")
                    continue
            
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

# ==========================================
# Frame Functions / Widgets
# ==========================================

def mainjokepage(parent):
    frame = Frame(parent)
    background = Label(frame, image=bg_joke_photo)
    background.place(x=0, y=0, relwidth=1, relheight=1)
    background.lower()

    test_frames = Frame(frame, bg="#FFFFFF", bd=0, highlightthickness=0)
    test_frames.place(relx=0.5, rely=0.6, anchor="center")

    spacing = Frame(test_frames, width=500, height=140, bg="#000000", bd=0, highlightthickness=0)
    spacing.pack_propagate(False)
    spacing.pack()
    test_label = Label(spacing, text="My text is here!", fg="#FFFFFF", bg="#000000", justify="center",)
    test_label.pack(expand=True)

    spacing1 = Frame(test_frames, width=500, height=120, bg="#CE0000", bd=0, highlightthickness=0)
    spacing1.pack_propagate(False)
    spacing1.pack(pady=(12, 0))
    test_label2 = Label(spacing1, text="My text is here!", fg="#FFFFFF", bg="#CE0000", justify="center",)
    test_label2.pack(expand=True)
    return frame


pages["home"] = mainjokepage(realframe)

showpagef("home")
root.mainloop()