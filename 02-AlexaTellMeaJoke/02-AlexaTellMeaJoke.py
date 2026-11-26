from tkinter import *
import random
from PIL import Image, ImageTk

root = Tk()
root.geometry("800x600")
root.title("Joke Teller - Haha")
root.resizable(0, 0)

bg_joke_teller = Image.open(Path(__file__).parent / "resources" / "bg_joke_teller.png")
bg_joke_photo = ImageTk.PhotoImage(bg_joke_teller)

container = Frame(root)
container.grid(row=0, column=1, sticky="nsew")
container.config(width=600, height=600)
pages = {}

def mainjokepage(parent):
    frame = Frame(root)
    background = Label(frame, image=bg_joke_photo)
    background.place(x=0, y=0, rewidth=1, reheight=1)
    background.lower()


pages["home"] = mainjokepage(container)

root.mainloop()