lista = list(range(10))

mensajes = ('Original:',
            'En posicipones pares:',
            'En posiciones impares:',
            'Al revés:',
            'Primera mitad:',
            'Segunda mitad:',
            'El del medio:',
            'El primero:',
            'El último:',)

operaciones = (lista,
               lista[0::2],
               lista[1::2],
               lista[::-1],
               lista[:len(lista)//2],
               lista[len(lista)//2::],
               lista[len(lista)//2],
               lista[0],
               lista[-1],)


mostrar = dict(zip(mensajes, operaciones))
for a, b in mostrar.items():
    print(a, '-->', b)
input()
