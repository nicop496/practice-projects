monedas = {'peso':'$','dolar':'US$','euro':'€',  'yen':'¥',}
pedido = input('Introduce una divisa: ')
for a,b in monedas.items():
    if a == pedido:
        print(b)
        break
else: print('No lo sé')

# currencies = {'Euro':'€', 'Dollar':'$', 'Yen':'¥'}
# currency = input("Introduce una divisa: ")
# print(currencies.get(currency.title(), "La divisa no está."))

input()