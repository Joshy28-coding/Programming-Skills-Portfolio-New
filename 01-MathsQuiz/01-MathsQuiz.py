print("Real Written Code by me.")
# - Hello! I am determined to write the code with the use of the lecturer's materials and non-A.I online references. (To be mentioned in the development document.)
# - Create a MathQuiz with the use of Tkinter interface.
# = HelloWorld("print")

from tkinter import *

root = Tk()
root.geometry("900x600")

# =====================================
# Main home screen frame
# ====================================

def mainhomescreenframe():
    frame = Frame(root)
    panel = Frame(frame, bg="#123456")
    panel.pack(padx=40, pady=40, fill="both", expand="true")

root.mainloop()