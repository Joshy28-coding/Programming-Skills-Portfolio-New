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
    "title": ("Courier New", 16),
    "heading": ("Courier New", 14),
    "body": ("Courier New", 12),
    "body_bold": ("Courier New", 12, "bold"),
}

# ====================================
# Application Root
# ====================================

root = Tk()
root.geometry("900x600")
root.title("Arithmetic Math Quiz")

root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

sidebar_main = Frame(root, width=300, bg=COLORS["bg_card_inner"])
sidebar_main.grid(row=0, column=0, sticky="ns")
sidebar_main.grid_propagate(False)

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
        sidebar, text="Difficulty Selector",
        fg=COLORS["fg_text"], bg=COLORS["bg_card_inner"],
        font=FONTS["body_bold"],
    )
    difficultyhead.grid(row=0, column=0, sticky="ew", padx=10, pady=30)
    
    home_btn = Button(
        sidebar, text="Home",
        fg=COLORS["fg_text"], bg=COLORS["bg_card"],
        font=FONTS["body_bold"], height=2
    )
    home_btn.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    main_btn = Button(
        sidebar, text="Main",
        fg=COLORS["fg_text"], bg=COLORS["bg_card"],
        font=FONTS["body_bold"], height=2
    )
    main_btn.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

    info_btn = Button(
        sidebar, text="Information",
        fg=COLORS["fg_text"], bg=COLORS["bg_card"],
        font=FONTS["body_bold"], height=2
    )
    info_btn.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

    return sidebar

sidebar = difficultysidebar()
sidebar.pack(fill="both", expand=True)

def mainhomescreen(parent):
    frame = Frame(parent, bg=COLORS["bg_color"])
    Label(frame, text="Arithmetic Math Quiz", bg=COLORS["bg_color"], fg=COLORS["fg_text"], font=FONTS["title"]).pack(pady=(150, 10))
    Label(frame, text="Welcome to the Quiz!", bg=COLORS["bg_color"], fg=COLORS["fg_text"], font=("Courier New", 26, "bold")).pack(pady=10)
    Label(frame, text="Choose your challenge tier. Each tier has 10 questions each.\n"
             "Earn 10 points on your first attempt, or 5 points on your second.",
        bg=COLORS["bg_color"], fg=COLORS["fg_text"], font=FONTS["body"], justify="center").pack(pady=10)
    Button(frame, text="Start quiz", command=lambda: show_page("quiz")).pack()
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