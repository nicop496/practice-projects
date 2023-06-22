import numpy as np

print("Matriz original:")
lista = [ [-44,   12], 
           [12.0,  51], 
           [1300, -5.0]]
matriz = np.array(lista)
print(matriz)


print('Restarle 5 a la segunda fila de la matriz:')
matriz[1,:] -= 5
print(matriz)

print('Multiplicar por 2 toda la matriz:')
matriz *= 2
print(matriz)

print('Dividir por -5 las dos primeras filas de la matriz:')
matriz[:1, :] /= -5
print(matriz)

print('Imprimir la ultima fila de la matriz:')
print(matriz[-1,:])

print('Promedio de toda la matriz:')
print(matriz.mean())

print('Suma de las ultimas dos columnas:')
print(np.sum(matriz[:,-2]))

input()