array = [[1,2,3,4],
         [5,6,7,8],
         [9,10,11,12],
         [13,14,15,16]]

# 00 01 02 03 04
# 10 11 12 13 14
# 20 21 22 23 24
# 30 31 32 33 34
# 40 41 42 43 44

def range_(a, b):
    """
    Examples:
    range_(1, 5) -> [1, 2, 3, 4, 5]
    range_(3, 3) -> [3]
    range_(10, 6) -> [10, 9, 8, 7, 6]
    """
    if a == b:
        return [a]
    if a < b:
        return list(range(a, b+1))
    if a > b:
        return list(range(a, b-1, -1))    

    
def snail(snail_map):
    if snail_map == [[]]: return []
    n = len(snail_map)
    snail_array = []

    def check():
        return len(snail_array) == n*n
    
    # Counters
    #Increase by 1
    x1_0 = 0
    x1_1 = 1 
    x1_2 = 2
    
    #Increase by 2
    x2_0 = 0 
    x2_1 = 1 
    x2_2 = 2 

    while True:
        # Up    
        snail_array += zip([x1_0] * (n-x2_0), #fila
                           range_(x1_0, n-x1_1)) #columna
        if check(): break

        # Right
        snail_array += zip(range_(x1_1, n-x1_1),
                           [n-x1_1] * (n-x1_1))
        if check(): break

        # Down
        snail_array += zip([n-x1_1] * (n-x2_1), 
                           range_(n-x1_2, x1_0))
        if check(): break

        # Left
        snail_array += zip(range_(n-x1_2, x1_1),
                           [x1_0] * (n-x2_2))
        if check(): break


        # Increase the counters
        x1_0 += 1
        x1_1 += 1
        x1_2 += 1

        x2_0 += 2
        x2_1 += 2
        x2_2 += 2        


    return [snail_map[row][column] for row, column in snail_array]

print(array)
input(snail(array))
