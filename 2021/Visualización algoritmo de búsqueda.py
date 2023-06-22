import pygame

pygame.init()
pygame.font.init()
pygame.display.set_caption('Algoritmo de búsqueda')

SCREEN_SIZE = int(input('\nIntroduce el ancho/alto de la ventana (en pixeles): '))
CELL_SIZE = int(input('Ahora introduce el ancho/alto de cada cuadradito (en pixeles): '))
AUTOMATIC = False if input('¿Automático o manual? (a/m): ') == 'm' else True
SCREEN_SIZE -= SCREEN_SIZE % CELL_SIZE
MAP_SIZE = SCREEN_SIZE // CELL_SIZE
FONT = pygame.font.SysFont('Serif', CELL_SIZE)

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (150, 150, 255)

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

class Wall:
    def __init__(self, mouse_pos):
        self.rect = (mouse_pos[0] - mouse_pos[0] % CELL_SIZE,
                     mouse_pos[1] - mouse_pos[1] % CELL_SIZE,
                     CELL_SIZE,
                     CELL_SIZE)
        self.row = mouse_pos[1] // CELL_SIZE
        self.column = mouse_pos[0] // CELL_SIZE


class Flag(Wall):
    def __init__(self, mouse_pos):
        super().__init__(mouse_pos)
        

class Searcher:
    def __init__(self, lenght, father, row, column):
        self.lenght = lenght
        self.father = father
        self.row = row
        self.column = column
        self.path = False

    def send_signal(self):
        self.path = True
        if type(self.father) == Searcher:
            self.father.path = True
            self.father.send_signal()


class PathFindingAlgorithm:
    def __init__(self, automatic = True):
        self.automatic = automatic #self.manual = not automatic
        self.quit = False
        self.map = []
        for _ in range(MAP_SIZE):
            self.map.append([0 for _ in range(MAP_SIZE)])
        self.flags = []
        self.walls = []
        self.searchers = []
        self.ready_to_draw_walls = False
        self.search_has_initated = False
        self.r = 0
        self.c = -1
    
    def events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_btns = pygame.mouse.get_pressed(3)
        taken_boxes = list(map(lambda x: x.rect, self.walls)) + list(map(lambda x: x.rect, self.flags))
        keys = pygame.key.get_pressed()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.quit = True
            
            # Encontrar el camino (si es automático)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and not self.search_has_initated and self.automatic:
                    
                    self.automatic_search()
                    self.search_has_initated = True            

            # Crear las banderas
            if e.type == pygame.MOUSEBUTTONDOWN:
                new_flag = Flag(mouse_pos)
                if len(self.flags) < 2 and not new_flag.rect in taken_boxes: 
                    self.flags.append(new_flag)
                    self.map[new_flag.row][new_flag.column] = new_flag
                
            # Saber si se pueden crear paredes
            if e.type == pygame.MOUSEBUTTONUP and len(self.flags) == 2 and not self.ready_to_draw_walls:
                self.ready_to_draw_walls = True
            
        
        if not self.search_has_initated:
            # Crear las paredes
            if mouse_btns[0]:
                new_wall = Wall(mouse_pos)
                if self.ready_to_draw_walls and not new_wall.rect in taken_boxes:
                    self.walls.append(new_wall)
                    self.map[new_wall.row][new_wall.column] = new_wall

            # Borrar las paredes
            if mouse_btns[2]:
                for wall in self.walls:
                    if list(wall.rect[:2]) == [mouse_pos[i]-mouse_pos[i]%CELL_SIZE for i in range(2)]:
                        self.walls.remove(wall)
                        self.map[wall.row][wall.column] = 0

        # Dejar presionado enter para buscar
        if keys[pygame.K_RETURN] and not self.automatic:
            if len(self.flags) == 2:
                self.manual_search()

    def draw(self):
        screen.fill(WHITE)
        
        # Banderas
        for flag in self.flags:
            pygame.draw.rect(screen, RED, flag.rect)
        
        # Muros
        for wall in set(self.walls):
            pygame.draw.rect(screen, BLACK, wall.rect)
        
        # Buscadores
        for searcher in self.searchers:
            color = LIGHT_BLUE if not searcher.path else BLUE
            pos_x = searcher.column * CELL_SIZE
            pos_y = searcher.row * CELL_SIZE
            pygame.draw.rect(screen, color, (pos_x, pos_y, CELL_SIZE, CELL_SIZE))

            text = FONT.render(str(searcher.lenght), 0, BLACK)
            screen.blit(text, (pos_x, pos_y))
        
        # Líneas
        for coord in range(0, SCREEN_SIZE, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (coord, 0), (coord, SCREEN_SIZE))
            pygame.draw.line(screen, BLACK, (0, coord), (SCREEN_SIZE, coord))
    
        pygame.draw.rect(screen, RED, (self.c * CELL_SIZE, self.r * CELL_SIZE, CELL_SIZE, CELL_SIZE), width=2)

    def manual_search(self):
        try:
            #simulación de un bucle
            self.c += 1
            if self.c == MAP_SIZE:
                self.c = 0
                self.r += 1
            if self.r == MAP_SIZE:
                self.r = 0

            return self.search(self.r, self.c)

        except IndexError:
            None

    def automatic_search(self):
        for _ in range(MAP_SIZE * len(self.map)):
            for r in range(MAP_SIZE):
                for c in range(MAP_SIZE):
                    if self.search(r, c):
                        print('LISTO')
                        return

        print ('\nNo existe ningún camino posible')

    
    def search(self, r, c):
        current_box_is_first_flag = self.map[r][c] == self.flags[0]
        current_box_is_searcher = type(self.map[r][c]) == Searcher

        if current_box_is_first_flag or current_box_is_searcher:
            for box in self.get_adjacent_boxes(r, c):
                try:
                    if box[0] >= 0 and box[1] >= 0:
                        if current_box_is_first_flag:
                            if self.map[box[0]][box[1]] == 0:
                                new_searcher = Searcher(1, self.map[r][c], box[0], box[1])
                                self.map[box[0]][box[1]] = new_searcher
                                self.searchers.append(new_searcher)

                            if self.map[box[0]][box[1]] == self.flags[1]:
                                self.searchers.clear()
                                return True

                        if current_box_is_searcher:
                            if self.map[box[0]][box[1]] == 0:
                                new_searcher = Searcher(self.map[r][c].lenght + 1, self.map[r][c], box[0], box[1]) 
                                self.map[box[0]][box[1]] = new_searcher
                                self.searchers.append(new_searcher)
                            
                            if self.map[box[0]][box[1]] == self.flags[1]:
                                self.map[r][c].send_signal()
                                return True
                        
                        if not self.automatic: pygame.draw.rect(screen, ORANGE, (box[1] * CELL_SIZE, box[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), width=2)

                except IndexError:
                    None #ocurriría IndexError si busca fuera del mapa

        return False

    def get_adjacent_boxes(self, r, c):
        """
        Devuelve la posiciones (fila y columna) de
        cada casilla adyacente de la posición 
        indicada por los parámetros
        -------------
        int : r = row (fila)
        int : c = column (columna)
        """
        return ((r-1, c-1), (r-1, c), (r-1, c+1),
                (r,   c-1),           (r,   c+1),
                (r+1, c-1), (r+1, c), (r+1, c+1))
        # return (            (r-1, c),
        #         (r,   c-1),            (r,   c+1),
        #                     (r+1, c),)


##########################
program = PathFindingAlgorithm(automatic=AUTOMATIC)
while not program.quit:
    program.draw()
    program.events()
    pygame.display.flip()
pygame.quit()
