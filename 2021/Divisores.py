print('='*8, 'DIVISORES', '='*8)
nums = input('Introduce los números que quieras separados por comas: ').split(',')
for i in range(len(nums)):
    nums[i] = int(nums[i])

def divisores(nums):
    divs = []
    for n in nums:
        div = [i for i in range(1, n+1) if n % i == 0]
        divs.append(div)
    return divs

for num, divs in zip(nums, divisores(nums)): print(f"{num} - {divs}")
