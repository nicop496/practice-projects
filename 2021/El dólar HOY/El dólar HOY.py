import requests
from bs4 import BeautifulSoup
from datetime import date
from tkinter import *
from tkinter import messagebox

# Constantes
WIDTH = 500
HEIGHT = 300
URL = 'https://www.dolarhoy.com/'

# Funciones
def calcular():
    try:
        for i in range(len(dolar_hoy)):
            
            if precios[i][0]:
                c = str(round(eval(f'{precios[i][0]}*({mult_var.get()})'), 2))
                canvas.itemconfig('txt_precio_comprar_' + str(i), text=c)
                
            v = str(round(eval(f'{precios[i][1]}*({mult_var.get()})'), 2))
            canvas.itemconfig('txt_precio_vender_' + str(i), text=v)
            
    except:
        messagebox.showerror('Error', 'Entrada incorrecta, debes\nintroducir un número o un cálculo.')
        
    
try:
    # Web Sraping
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'lxml')

    tipos = soup.find_all(class_='title')
    
    precios = []
    for p in soup.find_all(class_='values'):
        sep = p.text.split('Venta')
        precios.append([sep[0][7:], sep[1][1:]])

    dolar_hoy = {tipo.text : precio for tipo, precio in zip(tipos, precios)}


    tipos = list(dolar_hoy.keys())
    precios = list(dolar_hoy.values())
    
    # Ventana
    root = Tk()
    root.title(f'Precio del dolar en Argentina el {date.today()}')
    root.resizable(False, False)
    
    # Icono
    try:
        root.iconbitmap('icono de dinero.ico')

    except TclError:
        messagebox.showinfo('Aviso', 'No se encontró el ícono (el archivo es "icono de dinero.ico")')

    finally:
        # Canvas
        canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        canvas.grid(columnspan=100)

        canvas.create_line(225, 0, 225, HEIGHT)
        canvas.create_line(0, 50, WIDTH, 50)
        canvas.create_line(225, 25, WIDTH,25)
        canvas.create_line(375, 25, 375, HEIGHT)

        canvas.create_text(112.5, 25, text='Tipo', font=1)
        canvas.create_text(375, 15, text='Precio', font=1)
        canvas.create_text(300, 37.5, text='Compra', font=1)
        canvas.create_text(440, 37.5, text='Venta', font=1)

        for i in range(len(dolar_hoy)):
            canvas.create_text(100, 75+i*50, text=tipos[i], font=1)
            canvas.create_text(300, 75+i*50, text=precios[i][0], font=1, tag='txt_precio_comprar_' + str(i))
            canvas.create_text(440, 75+i*50, text=precios[i][1], font=1, tag='txt_precio_vender_' + str(i))

        # Margen de abajo
        Button(root, text='Info', padx=20, command=lambda: messagebox.showinfo('Info', f'Datos sacados de {URL}')).grid(row=1, column=0)
        
        Label(root, text='x', font=1).grid(row=1, column=97)
        
        mult_var = StringVar(root, value=1)
        mult = Entry(root, bg='white', font=1, textvariable=mult_var, width=12)
        mult.grid(row=1, column=98)
        
        Button(root, text='Calcular', padx=5, command=calcular).grid(row=1, column=99)

        root.mainloop()

except ConnectionError:
    messagebox.showerror('Error', 'Hay problemas de conexión')

except:
    messagebox.showerror('Error', 'Ocurrió un error inesperado')
    root.destroy()
    raise