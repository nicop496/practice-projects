def secuencia(n):
    if n < 1:
        raise ValueError('Introduce un numero natural')
    else:
        nums = [n]
        
        while nums[-1] != 1:
            if nums[-1]%2 == 0:
                nums.append(nums[-1]//2)
            else:
                nums.append(nums[-1]*3+1)
        
        return nums

print('Si el numero es par entonces el siguiente numero es la mitad del ultimo; si es impar\nentonces se multiplica por 3 y se le suma 1.\nLo interesante es que la secuencia siempre termina en 1')
print(secuencia(int(input('Introduce un numero: '))))
q = input('')
