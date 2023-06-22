pregunta = input ('¿Cuánta batería tenés? ')
valor = int (pregunta)
if valor <= 20 and valor > 0 :
    print ('Poné a cargar tu dispositivo')
if valor >= 21 and valor < 100:
    print ('Ok, no pasa nada')
if valor < 0:
    print ('Me estas mintiendo descaradamente')
if valor > 100:
    print ('IMPOSIBLE')
quedarse = input ("")
