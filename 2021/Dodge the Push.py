import pygame
import random



STARTING_DIFFICULTY = 1 # Dificultad (cada cuanto tiempo salen nuevos obstáculos) inicial
CHANGE_DIFFICULTY_TIME_PERIOD = 15 # Cada cuantos segundos cambia la dificultad
DIFFICULTY_CHANGE = 0.05 # Cuanto cambia la dificultad
LIMIT_DIFFICULTY = 0.5 # Límite de dificultad
#LIMIT_DIFFICULTY tiene que ser divisible por DIFFICULTY_CHANGE

OBSTACLES_SPACING = 5 # Espacio entre los obstáculos
OBSTACLE_WIDTH = 75 # Ancho de los obstáculos
OBSTACLES_PER_ROW = 5 # Obstáculos posibles por fila
WIDTH = OBSTACLE_WIDTH * OBSTACLES_PER_ROW + OBSTACLES_SPACING
HEIGHT = 650 # Alto de la ventana
FONT_NAME = 'Century Gothic' # Nombre del tipo de letra
TITLE = 'Dodge the Push' # Título de la ventana
FPS = 60 # Máxima cantidad de fotogramas por segundo

# Colores
WHITE = 255, 255, 255
PLAYER_RED = 173, 46, 39
OBSTACLE_BLUE = 54, 54, 135
BG = 10, 10, 10

def draw_text(window, msg, center, size, color, bold=False, italic=False, bgcolor=None):
    font = pygame.font.SysFont(FONT_NAME, size, bold, italic)
    for idx, line in enumerate(msg.split('\n')):
        idx -= len(msg.split('\n')) / 2
        text = font.render(line, True, color, bgcolor)
        rect = text.get_rect(centerx = center[0], centery = center[1] + size * idx)
        window.blit(text, rect.topleft)


class Obstacle(pygame.sprite.Sprite):
    WIDTH = OBSTACLE_WIDTH - OBSTACLES_SPACING
    HEIGHT = 30

    def __init__(self, *groups):
        super().__init__(*groups)
        self.speed = random.randint(1, 5)
        self.image = pygame.Surface([self.WIDTH, self.HEIGHT]).convert()
        self.image.fill(OBSTACLE_BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(OBSTACLES_SPACING,
                                       WIDTH-self.image.get_width() + OBSTACLES_SPACING,
                                       self.image.get_width() + OBSTACLES_SPACING)
        self.rect.y = -self.image.get_height()

    def update(self):
        self.last_position = self.rect.bottom
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()
            return True
            

class Player(pygame.sprite.Sprite):
    WIDTH = WIDTH / 10
    HEIGHT = 50
    SPEED = 10.1
    velocity = 0

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface([self.WIDTH, self.HEIGHT]).convert()
        self.image.set_colorkey(WHITE)
        self.image.fill(PLAYER_RED)
        self.rect = self.image.get_rect()
        self.start_position()

    def update(self, obstacles):
        # Teclas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.velocity = self.SPEED
            #print('der')
        elif keys[pygame.K_LEFT]:
            self.velocity = -self.SPEED
            #print('izq')
        else: self.velocity = 0
        
        # Obstáculos por abajo
        for obs in pygame.sprite.spritecollide(self, obstacles, False):
            if obs.rect.bottom >= self.rect.top and obs.last_position <= self.rect.top:
                self.rect.y += obs.speed

        # Avanzar
        self.rect.x += self.velocity
        
        # Obstáculos por izquierda y derecha
        for obs in pygame.sprite.spritecollide(self, obstacles, False):
            if self.velocity > 0: self.rect.right = obs.rect.left
            if self.velocity < 0: self.rect.left = obs.rect.right

        # Paredes
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.left < 0: self.rect.left = 0

    def start_position(self):
        self.rect.center = [WIDTH / 2, HEIGHT / 2 - HEIGHT / 4]


def main():
    pygame.init()
    pygame.font.init()
    window = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    player = Player(all_sprites)
    difficulty_timer = score = obstacle_timer = 0
    scores = []
    difficulty = STARTING_DIFFICULTY
    game_over = paused = done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                #print('Salir')

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        game_over = False
                        #print('Reiniciar')
                else:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                        #print('Pausar')

        clock.tick(60)
        window.fill(BG)

        if not game_over:
            #si el juego está pausado no actualizar nada
            if paused:
                continue
            
            #actualizar al jugador
            player.update(obstacles)
            
            #si el jugador ya no es visible es game over
            if player.rect.y > HEIGHT:
                #print('GAME OVER')
                game_over = True
                obstacle_timer = difficulty_timer = score = 0
                difficulty = STARTING_DIFFICULTY
                for obstacle in obstacles:
                    obstacle.kill()
                player.start_position()

            #actualizar los obstáculos y aumentar la puntuación si desaparece algún obstáculo
            for obs in obstacles:
                if obs.update():
                    score += 1
                    scores.append(score)
                    #print('Punto')
                                
            #temporizadores
            difficulty_timer += 1
            obstacle_timer += 1
        
            #hacer el juego cada vez más díficil
            if difficulty_timer / FPS >= CHANGE_DIFFICULTY_TIME_PERIOD and difficulty > LIMIT_DIFFICULTY:
                difficulty_timer = 0
                difficulty -= DIFFICULTY_CHANGE
                #print('AUMENTO DE DIFICULTAD:', round(difficulty, 2))
            
            #crear nuevos obstáculos
            if obstacle_timer / FPS >= difficulty:
                obstacle_timer = 0
                Obstacle(all_sprites, obstacles)
                #print('Nuevo obstáculo')
    
            #dibujar
            draw_text(window, f'Score: {score}', [WIDTH-100, 30], 25, WHITE, bold=True)
            all_sprites.draw(window)

        else:
            draw_text(
                window, 
                f'Game Over\n\nScore: {scores[-1]}\nHigh score: {max(scores)}\nPress R to restart',
                [WIDTH / 2, HEIGHT / 2], 40, WHITE)

        pygame.display.flip()
    pygame.quit()
main()
