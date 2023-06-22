from math import log2
from random import choice, randint
from select_difficulty import select_difficulty


class Sudoku:
    def __init__(self, n):
        self.n = n
        self.completed_sudoku = self.__create_sudoku()
        self.to_solve = [list(i) for i in self.completed_sudoku]

        def gfboxes(section):
            """Gets the filled boxes of a row, column or square"""
            return [i for i in section if i]

        difficulty = select_difficulty(1, 3, 6) if self.n != 4 else 1
        for r in range(self.n):
            for c in range(self.n):

                count_row = len(gfboxes(self.to_solve[r]))
                count_col = len(gfboxes(self.get_column(self.to_solve, c)))
                count_sqr = len(gfboxes(self.get_square(self.to_solve, r, c)))
                total_filled_squares = count_row + count_col + count_sqr
                
                posible_cases = self.n * 3 - total_filled_squares
                if posible_cases <= difficulty:
                    posible_cases = difficulty

                if randint(difficulty, posible_cases) == difficulty:
                    self.to_solve[r][c] = 0

    def create_sudoku(self):
        sudoku = []
        for _ in range(self.n): 
            sudoku.append([0 for _ in range(self.n)])

        for row in range(self.n):
            for col in range(self.n):
                # numr_row = a number is repeated in the row (boolean)
                numr_row = sudoku[row].count(sudoku[row][col]) != 1
                numr_col = Sudoku.get_column(sudoku, col).count(sudoku[row][col]) != 1
                numr_sqr = Sudoku.get_square(sudoku, row, col).count(sudoku[row][col])
                box_is_free = sudoku[row][col] == 0

                posible_nums = list(range(1, self.n+1))
                while any([numr_row, numr_col, numr_sqr, box_is_free]):
                    if not posible_nums:
                        return# self.create_sudoku() # try again
                    num = choice(posible_nums)
                    sudoku[row][col] = num
                    posible_nums.remove(num)

        return tuple([tuple(i) for i in sudoku])

    def __create_sudoku(self):
            s = []
            for _ in range(self.n): s.append([i-i for i in range(self.n)])

            for r in range(len(s)):
                for c in range(len(s)):
                    posible_nums = list(range(1, self.n+1))

                    while any((
                        s[r].count(s[r][c]) != 1,
                        self.get_column(s, c).count(s[r][c]) != 1,
                        self.get_square(s, r, c).count(s[r][c]) != 1,
                        s[r][c] == 0)):
                        
                        try:
                            num = choice(posible_nums)
                        except IndexError:
                            return self.__create_sudoku()

                        s[r][c] = num
                        posible_nums.remove(num)

            return s

    @staticmethod
    def get_square(sudoku, row_num, column_num):
        sqr_size = int(log2(len(sudoku)))
        start_row = row_num - row_num % sqr_size
        start_col = column_num - column_num % sqr_size
        rows = range(start_row, start_row + sqr_size)
        cols = range(start_col, start_col + sqr_size)
        return [sudoku[r][c] for r in rows for c in cols]

    @staticmethod
    def get_column(sudoku, column_num):
        return [sudoku[row][column_num] for row in range(len(sudoku))]
    
    @staticmethod
    def get_row(sudoku, row_num):
        return sudoku[row_num]