from tkinter import Tk, Radiobutton, Button, IntVar


def select_difficulty(easy, medium, hard):
    root = Tk()
    root.title("Select difficulty")
    root.resizable(True, False)
    dificulty = IntVar()

    def ready_button():
        if dificulty.get():
            root.destroy()

    Radiobutton(root, text="Easy", variable=dificulty, value=easy).pack()
    Radiobutton(root, text="Medium", variable=dificulty, value=medium).pack()
    Radiobutton(root, text="Hard", variable=dificulty, value=hard).pack()

    Button(root, text="Done", command=ready_button).pack()

    root.mainloop()
    return dificulty.get()