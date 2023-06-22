palabra = input('Introduce una palabra: ')
for i in range(len(palabra)):print(palabra[:i+1])
for i in range(len(palabra)):print(palabra[:-i-1])

input()
