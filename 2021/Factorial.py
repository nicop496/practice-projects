def factorial(n):
    if n <= 1: return 1
    else: return n * factorial(n-1)

for i in range(1, 31): print(f'{i}! = {factorial(i)}')
print(factorial(int(input('Introduce un número: '))))
