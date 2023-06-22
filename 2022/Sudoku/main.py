import pygame
from button import Button
from sudoku import Sudoku
from display_text import display_text
from math import log2


WIN_SIZE = 648
MARGIN_SIZE = 50
NUMSEVENTS = (pygame.K_1, pygame.K_2, pygame.K_3, 
              pygame.K_4, pygame.K_5, pygame.K_6, 
              pygame.K_7, pygame.K_8, pygame.K_9)


class Main:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Sudoku")
        self.window = pygame.display.set_mode((WIN_SIZE, WIN_SIZE+MARGIN_SIZE))
        self.in_game = False

        # Create menu buttons
        self.menu_buttons = [
            Button(self.window, (110, 280), (115, 115), text="9 x 9"),
            Button(self.window, (415, 415), (170, 170), text="4 x 4")
        ]

        # Create margin buttons
        names = "Show completed", "New", "Back", "Quit"
        funcs = self.show_completed, lambda: self.get_ready(self.sudoku.n), self.__init__, self.quit
        amount = len(names)
        sizes = [(WIN_SIZE // amount, MARGIN_SIZE)] * amount
        positions = [(x, WIN_SIZE) for x in range(0, WIN_SIZE, WIN_SIZE // amount)]
        self.margin_buttons = [Button(self.window, p, s, f, n) for p, s, f, n in zip(positions, sizes, funcs, names)]


        # Main loop
        self.running = True
        while self.running:
            self.click_up = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click_up = True

            self.window.fill(pygame.Color("white"))
            if self.in_game:
                self.playing()
            else:
                self.menu_screen()
                
            pygame.display.flip()
        pygame.quit()
                    
    def menu_screen(self):
        # Title
        display_text(self.window, "SUDOKU", 96, (WIN_SIZE/2, WIN_SIZE/4))

        # 4x4 and 9x9 buttons
        for btn in self.menu_buttons:
            btn.draw(bold=True)
            btn.update(self.click_up)
            if btn.is_pressed:
                self.get_ready(int(btn.text[0]))

    def playing(self):
        # Draw thick lines (the other lines are made by the edges of the number boxes)
        sqr_size = int(log2(self.sudoku.n))
        for xy in range(0, WIN_SIZE + 1, self.box_size):
            if xy % (self.box_size * sqr_size):
                continue
            pygame.draw.line(self.window, pygame.Color("black"), (xy, 0), (xy, WIN_SIZE), width=6)
            pygame.draw.line(self.window, pygame.Color("black"), (0, xy), (WIN_SIZE, xy), width=6)

        # Draw and update margin buttons
        for btn in self.margin_buttons:
            btn.draw(size=24, italic=True, bold=True)
            btn.update(self.click_up)

        self.numbers_func() 

    def get_ready(self, n):
        """
        This method is called after pressing a menu button (the ones
        to start playing) and  before the game starts.
        """
        self.sudoku = Sudoku(n)
        self.box_size = WIN_SIZE // self.sudoku.n
        self.boxes = [[] for _ in range(self.sudoku.n)] 
        self.pressed_nums = []
        self.empty_boxes = []
        
        # Create boxes
        for row in range(self.sudoku.n):
            for col in range(self.sudoku.n):
                txt = str(self.sudoku.to_solve[row][col]) if self.sudoku.to_solve[row][col] else ''
                btn = Button(
                    self.window, 
                    (row*self.box_size, col*self.box_size),
                    [self.box_size]*2,
                    text=txt,
                    keep_pressed=True
                )

                self.boxes[row].append(btn)
                if not btn.text: 
                    self.empty_boxes.append(btn)

        self.in_game = True

    def numbers_func(self):        
        keys = pygame.key.get_pressed()
        
        # Iterate over all the number boxes
        for row in range(self.sudoku.n):
            for column in range(self.sudoku.n):
                num = self.boxes[row][column]
                if not num in self.empty_boxes:
                    num.draw()
                    continue

                num.draw(size=self.box_size//2, bold=True)
                num.update(self.click_up)

                if num.is_pressed:
                    self.pressed_nums.append(num) 
                
                if len(self.pressed_nums) > 1:
                    self.pressed_nums[0].is_pressed = False 
                    self.pressed_nums.pop(0)             

                if len(self.pressed_nums) == 1:
                    selected_box = self.pressed_nums[-1]
                    selected_box.color = pygame.Color("blue")

                    # Deselect
                    if self.click_up and not num.mouse_is_over:
                        self.pressed_nums.remove(selected_box)

                    # Numbers keys
                    for num_event in NUMSEVENTS[:self.sudoku.n]:
                        if keys[num_event]:
                            selected_box.text = str(NUMSEVENTS.index(num_event)+1)
                            self.sudoku.to_solve[row][column] = NUMSEVENTS.index(num_event)+1

                    # Delete key
                    if keys[pygame.K_BACKSPACE] and selected_box.text:
                        selected_box.text = ""
                        self.pressed_nums.remove(selected_box)
                        self.sudoku.to_solve[row][column] = 0

    def show_completed(self):
        for row in range(self.sudoku.n):
            for col in range(self.sudoku.n):
                num_btn = self.boxes[row][col]
                if num_btn in self.empty_boxes:
                    num_btn.text = str(self.sudoku.completed_sudoku[row][col])

    def quit(self):
        self.running = False

if __name__ == "__main__":
    Main()
