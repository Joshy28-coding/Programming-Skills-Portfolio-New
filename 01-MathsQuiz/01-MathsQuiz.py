from tkinter import *

COLORS = {
    # ! - Background Colors
    "bg_color": "#0B0F19",  # Background color
    "bg_card": "#111827",  # Card Container
    "bg_card_inner": "#1F2937",  # Inner Card Container
    "bg_entry": "#0F172A",  # Dark Entry Card
    
    # ! - Text Colors
    "fg_text": "#F9FAFB",  # White Text
    "fg_muted": "#9CA3AF",  # Muted Grey Text
}

FONTS = {
    "title": ("Helvetica", 16),
    "heading": ("Helvetica", 14),
    "body": ("Helvetica", 12),
    "body_bold": ("Helvetica", 12, "bold"),
}

root = Tk()
root.geometry("900x600")
root.title("Arithmetic Math Quiz")

container = Frame(root)
container.pack(fill="both", expand=True)

pages = {}

def show_page(name):
    for page in pages.values():
        page.pack_forget()

    pages[name].pack(fill="both", expand=True)

def make_home_page(parent):
    # Create a frame, then put widgets inside it.
    frame = Frame(parent, bg=COLORS["bg_color"])

    Label( frame, text="Welcome to the quiz!", bg="#0B0F19", fg="white").pack(pady=20)

    Button(
        frame,
        text="Start quiz",
        command=lambda: show_page("quiz")
    ).pack()

    return frame

def make_quiz_page(parent):
    frame = Frame(parent, bg="#1F2937")

    Label(
        frame,
        text="Question 1: What is 2 + 2?",
        bg="#1F2937",
        fg="white"
    ).pack(pady=20)

    Button(
        frame,
        text="Back to home",
        command=lambda: show_page("home")
    ).pack()

    return frame

pages["home"] = make_home_page(container)
pages["quiz"] = make_quiz_page(container)

show_page("home")
root.mainloop()