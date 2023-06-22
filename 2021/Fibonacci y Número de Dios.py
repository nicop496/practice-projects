def fib(n):
    nums = [0,1]
    cociente = []
    if n <= 1:
        return nums
    else:
        for _ in range(n-2):
            nums.append(sum(nums[-2:]))
            cociente.append(nums[-1]/ nums[-2])   
        return nums, cociente

print(fib(int(input('Digite un número: '))))

q = input()
