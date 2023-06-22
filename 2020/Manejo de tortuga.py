import turtle


for ramón in range (1, 10000):
    tecla = input ('''Controles:
-Movimiento: flechas
-Colores: Escribir el color
-Grosor de lápiz: Escribir el número de grosor (máximo 3)
''')
 
    if tecla == ('amarillo'):
        turtle.pencolor ('yellow')
    if tecla == ('rojo'):
        turtle.pencolor ('red')
    if tecla == ('azul'):
        turtle.pencolor ('blue')
    if tecla == ('verde'):
        turtle.pencolor ('green')
    if tecla == ('violeta'):
        turtle.pencolor ('violet')
    if tecla == ('blanco'):
        turtle.pencolor ('white')
    if tecla == ('negro'):
        turtle.pencolor ('black')
    if tecla == ('1'):
        turtle.pensize (2)
    if tecla == ('2'):
        turtle.pensize (3)
    if tecla == ('3'):
        turtle.pensize (4)

quedarse = input ('')

window = turtle.Screen()
flecha = turtle.Turtle()

def arriba():
   flecha.setheading(90)
   flecha.forward(100)

def derecha():
   flecha.setheading(0)
   flecha.forward(100)

def abajo():
   flecha.setheading(270)
   flecha.forward(100)

def izquierda():
   flecha.setheading(180)
   flecha.forward(100)


window.onkeypress(arriba, "Up")
window.onkeypress(derecha, "Right")
window.onkeypress(abajo, "Down")
window.onkeypress(izquierda, "Left")

window.listen()
