##print('='*8, 'MÚLTIPLOS', '='*8)
##cuantos = int(input('¿Cuántos múltiplos queres de cada número?  '))
##nums = input('Bien, ahora introduce los números que quieras separados por comas: ').split(',')
##for n in nums:
##    n = int(n)
##    print(n, '-', [n*multiplo for multiplo in range(2, cuantos+1)], '\n')

cuantos = int(input(f'{"="*8} MÚLTIPLOS {"="*8}\n¿Cuántos múltiplos queres de cada número?  '))
for n in input('Bien, ahora introduce los números que quieras separados por comas: ').split(','): print(int(n), '-', [int(n)*multiplo for multiplo in range(2, cuantos+1)], '\n')
