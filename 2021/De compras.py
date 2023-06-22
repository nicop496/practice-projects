carrito = {}
total = 0
print('LISTA COMPRAS')
while input('¿Acabar? (si/no) ') == 'no':
    producto = input('producto: ')
    precio = float(input('precio: '))
    total += precio
    carrito[producto] = precio
print('\nLista de compras\n================')
for a,b in carrito.items():
    print(a, '-->',b)
print(f'----------------\nCoste total: {total}')
input()