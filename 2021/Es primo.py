def primo (n):
    for nums in range(2, n):
        if n % nums == 0:
            return False
    else:
        return True

input(primo(int(input('Introduce un número: '))))
