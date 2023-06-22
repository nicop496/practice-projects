import numpy as np
oracion = input('Introduce una oración: ').split()
largos = []
for i in oracion: largos.append(len(i))
print(np.mean(largos))
input()