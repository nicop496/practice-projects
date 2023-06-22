import shutil
import os
import re
from bs4 import BeautifulSoup
import requests

# Preguntar la ubicacion de donde se quiere la carpeta
pregunta = input('Introduce una ubicación de la computadora: ')
ubicacion_carpeta = f"{pregunta}/☠auto-halloween☠/"

# Conseguir el html de la página con los dibujos
r = requests.get('https://asciiart.website/index.php?art=holiday/halloween')
soup = BeautifulSoup(r.text, 'lxml')

# Extraer los dibujos que quiero
dibujos = []
for i in range(31, 51):
    dibujos.append(soup.find('pre', id=f'p{i}').find(text=True).rstrip('\n'))
    
def crear_todo():
    # Crear la carpeta
    os.mkdir(ubicacion_carpeta)

    # Crear los archivos .txt
    for i in range(len(dibujos)):
        # Ubicacion de cada archivo
        archivo_txt = f'{ubicacion_carpeta}☠{i}.txt'
        # Crearlos
        with open(archivo_txt, 'w') as file: file.write(dibujos[i])
        # Leerlos
        with open(archivo_txt, 'r') as file: lineas = file.readlines()
        # Quitar las lineas vacias
        with open(archivo_txt, 'w') as file:
            for linea in lineas:
                if not linea == '\n':
                    file.write(linea)

# Intentar crear la carpeta y los archivos
try: crear_todo()          
# Pero si ya existen borrarlos 
except FileExistsError:
    shutil.rmtree(ubicacion_carpeta)

except:
    shutil.rmtree(ubicacion_carpeta)
    raise
