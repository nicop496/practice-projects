from tkinter import *
from math import *

def resultado():
    try:
        r = eval(pantalla.get())
        pantalla.delete(0, last=END)
        pantalla.insert(0, str(r))
    except:
        if pantalla.get():
            pantalla.delete(0, last=END)
            pantalla.insert(0, 'Error')

            
window = Tk()
window.title('Calculadora')
window.resizable(False, False)
root = Frame(window, bg='#335262')
root.pack()
pantalla = Entry(root, font='Consolas 20', bd=3, bg='#EFEDDC')#'#E6E6E6')
pantalla.grid(padx=10, pady=10, columnspan=40)

# Crear los botones
b = ['DEL', '⌫ ', ' = ', ' , ',
     ' 1 ', ' 2 ', ' 3 ', ' × ',
     ' 4 ', ' 5 ', ' 6 ', ' ÷ ',
     ' 7 ', ' 8 ', ' 9 ', ' + ',
     ' ( ', ' 0 ', ' ) ', ' - ',
     ]

btns = [Button(root, text=b[i], padx=6, pady=4,
               font='Consolas 17', bg='#6A8A91',
               fg='white', activebackground='#EA9860') for i in range(len(b))]

# Posicionar los botones
i = 0
for r in range(5):
    for c in range(4):
        btns[i].grid(row=r+1, column=c, padx=5, pady=5)
        i += 1

# Darles funcionamiento a los botones
btns[0].config(command = lambda: pantalla.delete(0, last=END))
btns[1].config(command = lambda: pantalla.delete(len(pantalla.get())-1))
btns[2].config(command = resultado)
btns[3].config(command = lambda: pantalla.insert(END, '.'))
btns[4].config(command = lambda: pantalla.insert(END, '1'))
btns[5].config(command = lambda: pantalla.insert(END, '2'))
btns[6].config(command = lambda: pantalla.insert(END, '3'))
btns[7].config(command = lambda: pantalla.insert(END, '*'))
btns[8].config(command = lambda: pantalla.insert(END, '4'))
btns[9].config(command = lambda: pantalla.insert(END, '5'))
btns[10].config(command = lambda: pantalla.insert(END, '6'))
btns[11].config(command = lambda: pantalla.insert(END, '/'))
btns[12].config(command = lambda: pantalla.insert(END, '7'))
btns[13].config(command = lambda: pantalla.insert(END, '8'))
btns[14].config(command = lambda: pantalla.insert(END, '9'))
btns[15].config(command = lambda: pantalla.insert(END, '+'))
btns[16].config(command = lambda: pantalla.insert(END, '('))
btns[17].config(command = lambda: pantalla.insert(END, '0'))
btns[18].config(command = lambda: pantalla.insert(END, ')'))
btns[19].config(command = lambda: pantalla.insert(END, '-'))


root.mainloop()
