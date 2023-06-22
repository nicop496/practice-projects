import turtle
turtle.shape("turtle")
pregunta = input ('¿Cuánta batería tenés? ')
valor = int (pregunta)
if valor <= 20 and valor > 0 :
    print ('Poné a cargar tu dispositivo')
    turtle.forward(valor)
if valor >= 21 and valor < 100:
    print ('Ok, no pasa nada')
    turtle.forward(valor)
if valor < 0:
    print ('Me estas mintiendo descaradamente')
if valor > 100:
    print ('IMPOSIBLE')
quedarse = input ("")
