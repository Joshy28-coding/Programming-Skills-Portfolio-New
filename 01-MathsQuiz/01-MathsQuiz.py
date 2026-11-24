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
container.grid(column=1)
container.config(width=600, height=600)

sidebar_main = Frame(root)
sidebar_main.grid(column=0)
sidebar_main.config(width=300, height=600)

pages = {}

def show_page(name):
    for page in pages.values():
        page.pack_forget()

    pages[name].pack(fill="both", expand=True)

def make_options_sidebar():
    sidebar = Frame(sidebar_main, bg=COLORS["bg_card_inner"])
    
    #Create home button
    home_btn = Button(sidebar, text='Home', font=('Bold',12), fg='#ffffff',bg='#22263d',bd=0,
                     command=home_page)
    home_btn.place(x=10, y=50)


    #Create main button
    main_btn = Button(sidebar, text='Main', font=('Bold',12), fg='#ffffff',bg='#22263d',bd=0,
                     command=main_page)
    main_btn.place(x=10, y=100)

    #Create info button
    info_btn = Button(sidebar, text='Information', font=('Bold',12), fg='#ffffff',bg='#22263d',bd=0,)
    info_btn.place(x=10, y=150)

    return sidebar

def make_home_page(parent):
    # Create a frame, then put widgets inside it.
    frame = Frame(parent, bg=COLORS["bg_color"])

    Label(frame, text="Welcome to the quiz!", bg=COLORS["bg_color"], fg=COLORS["fg_text"], font=FONTS["title"])

    Button(
        frame,
        text="Start quiz",
        command=lambda: show_page("quiz")
    )

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