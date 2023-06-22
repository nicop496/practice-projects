import requests
from bs4 import BeautifulSoup
from tkinter import *

def conjugar_verbo(verbo):
    url = f'https://pasttenses.com/{verbo}-past-tense'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    
    c = [v.text for v in soup.find_all(class_='tg-6k2t')[1:4]]
    
    txt.config(text='\n\n'.join(c))
    

root = Tk()
root.title('English verbs')
root.geometry('290x180')
verbo = Entry(root, bd=8)
verbo.pack()
Button(root, text='Conjugar', command=lambda: conjugar_verbo(verbo.get().lower())).pack()
txt = Label(root, font=1)
txt.pack()
Label(root, text='Datos extraídos de pasttenses.com').pack(side=BOTTOM)

root.mainloop()
