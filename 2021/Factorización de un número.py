def factorizar(n):
    cocientes = [n]
    factores = []
    while True:
        for i in range(2, 10):
            if cocientes[-1] % i == 0:
                factores.append(i)
                cocientes.append(cocientes[-1] // i)
                break
        else:
            factores.append(cocientes[-1])
            cocientes.append(cocientes[-1] // factores[-1])
            if factores[-1] == 1 and cocientes[-1] == 1:
                cocientes.pop(-1); factores.pop(-1)
            return(cocientes, factores)

print('='*8, 'Factorización de un número', '='*8)
input(factorizar(int(input('Introduce un número: '))))
