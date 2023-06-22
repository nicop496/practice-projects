from re import sub
from random import choices
from tkinter import *

def get_words():
    def get_list(file):
        return sub(r'\s+', ' ', file.read()).split()
        
    with open('lista de 100 sustantivos.txt', 'r', encoding='utf-8') as f:
        noun = choices(get_list(f))

    with open('lista de 200 adjetivos.txt', 'r', encoding='utf-8') as f:
        adjectives = choices(get_list(f), k=2)

    words = ' '.join(noun + adjectives).capitalize() 
    label['text'] = words


root = Tk()
root.geometry('225x50')
root.resizable(False, False)
label = Label(root)
Button(root, text='Click me!', command=get_words).pack()
label.pack()
root.mainloop()
