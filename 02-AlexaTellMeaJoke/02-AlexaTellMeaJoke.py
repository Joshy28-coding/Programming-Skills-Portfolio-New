from tkinter import *
import random
from pathlib import Path
from PIL import Image, ImageTk

root = Tk()
root.geometry("800x600")
root.title("Joke Teller - Haha")
root.resizable(0, 0)

bg_joke_teller = Image.open(Path(__file__).parent / "resources" / "bg_joke_teller.png")
bg_joke_photo = ImageTk.PhotoImage(bg_joke_teller)

realframe = Frame(root)
realframe.pack(fill="both", expand=True)
pages = {}

def show_page(name):
    for page in pages.values():
        page.pack_forget()

    pages[name].pack(fill="both", expand=True)

def mainjokepage(parent):
    frame = Frame(parent)
    background = Label(frame, image=bg_joke_photo)
    background.pack(fill="both", expand=True)

    return frame


pages["home"] = mainjokepage(realframe)

show_page("home")
root.mainloop()