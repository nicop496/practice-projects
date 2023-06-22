NONE = '_ '
QUEEN = 'Q '


def queen_is_posible(board, row_num, col_num):
    """Determina si la posición de la dama es válida."""
    board_size = len(board)
    row = [board[row_num][c] for c in range(board_size) if c != col_num]
    column = [board[r][col_num] for r in range(board_size) if r != row_num]
    top_left = [board[row_num-i][col_num-i] for i in range(1, row_num+1) if not row_num-i<0 and not col_num-i<0]
    top_right = [board[row_num-r][c] for r, c in zip(range(1, row_num+1), range(col_num+1, board_size))]
    bottom_left = [board[r][col_num-c] for r, c in zip(range(row_num+1, board_size), range(1, col_num+1))]
    bottom_right = [board[r][c] for r, c in zip(range(row_num+1, board_size), range(col_num+1, board_size))]
    diagonals = top_left + top_right + bottom_left + bottom_right

    attacking_squares = row + column + diagonals
    return not QUEEN in attacking_squares


def create_variation(board, row_num, column_num):
    """Crea una variación del tablero con la posición dada"""
    new_board = [list(row) for row in board.board]
    new_board[row_num][column_num] = QUEEN
    new_board = Board(new_board, board)
    return new_board


class Board:
    def __init__(self, board: list, father=None, fixed_queen=None):
        if fixed_queen:
            board[fixed_queen[0]][fixed_queen[1]] = QUEEN
        self.board = tuple([tuple(row) for row in board])
        self.father = father
        self.n = len(self.board)
        self.evaluated = False
        self.variations_created = False
        self.variations = None
    
    def __repr__(self):
        string = ''
        for row in self.board:
            string += str(row) + '\n'
        return string
    
    def evaluate(self):
        if self.variations_created:
            if all(map(lambda variation: variation.evaluated, self.variations)):
                self.evaluated = True
                return
            else:
                for variation in self.variations:
                    if not variation.evaluated:
                        variation.evaluate()
                        break
                return

        else:
            if self.create_variations():
                self.variations[0].evaluate()
                return
            else:
                self.evaluated = True
                return

    def create_variations(self):
        try:
            row_num = self.board.index(tuple([NONE]*self.n))
        except ValueError:
            self.queen_found(self.board)
            return
        self.variations_created = True
        queens_positions = [col_num for col_num in range(self.n) if queen_is_posible(self.board, row_num, col_num)]

        if queens_positions:
            self.variations = list(map(
                lambda column_num: create_variation(self, row_num, column_num), 
                queens_positions))
            return True
        else:
            return False

    def queen_found(self, solution):
        """Este método es llamado cuando se encuentra la solución"""
        if self.father:
            self.father.queen_found(solution)
        else:
            self.evaluated = True
            self.board = solution
            return

#######################################
def solve_n_queens(n, fixed_queen=None):
    board = Board([[NONE for _ in range(n)] for _ in range(n)], fixed_queen=fixed_queen)
    while not board.evaluated:
        board.evaluate()
    return board
    result = ''
    for row in board.board:
        result += ''.join(row) + '\n'
    return result if result.count(QUEEN) >= n else None


input(solve_n_queens(int(input('El tablero es de n x n. Introduce el valor de n: '))))
