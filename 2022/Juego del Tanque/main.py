import pygame, time, sys
from constantes import *
from clases_secundarias import *
from tanque import Tank
from funciones import *


class Game:
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.mouse.set_visible(False)
    pygame.display.set_caption('Juego del tanque')

    clock = pygame.time.Clock()
    done = False
    current_level = 0
    level_over =  False
    window = pygame.display.set_mode((WIDTH, HEIGHT), SCALED | HWSURFACE | RESIZABLE, 1)
    pause_mode = False
      
    def __init__(self):
        self.player = Tank(5, 25)
        
        self.LOSE = load_audio('perder')
        load_audio('música').play(loops=-1)

        self.load_level()

    def mainloop(self):
        pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN])
        while 1:
            self.draw_level()
            self.update_level()
            
            if self.pause_mode:
                self.window.blit(CURTAIN, (0,0))
                draw_text(self.window, 'PAUSA', CENTER, 60, WHITE, bold=True)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.pause_mode = False if self.pause_mode else True
                        pygame.mouse.set_visible(self.pause_mode)

                self.level_events(event)

            pygame.display.flip()
            self.clock.tick(FPS)

    def draw_level(self):
        self.window.fill(BG)
        for group in sprite_groups_list[:-1]: # Saco al último elemento de la lista (el grupo es 'walls',
            for sprite in group:              # que son los sprites con los que puede colisionar el tanque)
                if not is_visible(sprite):    # porque los sprites son repetidos de grupos anteriores
                    continue
                try:
                    sprite.draw(self.window)
                except AttributeError:
                    self.window.blit(sprite.image, sprite.rect.topleft)

        self.player.draw(self.window)

    def update_level(self):
        if self.pause_mode: return

        self.player.update(self.walls)
        bullets.update()
        shooters.update()
        blocks.update()
        animations.update()
        for shooter in smart_shooters:
            if is_visible(shooter):
                shooter.update(self.player.rect.center)     
        if self.player.bullets_collisions():
            self.new_level(restart=True)
            self.LOSE.play()
    
    def level_events(self, event):
        if self.pause_mode: return

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.player.shoot()
            
            if event.button == 3:
                self.new_level()

    def new_level(self, restart=False):
        for group in sprite_groups_list: group.empty()
        self.player.reset()
        self.current_level += 1 if not restart else 0
        self.load_level()

    def load_level(self):
        level_array = read_csv(f'assets/niveles/{self.current_level}.csv')

        for row_index, row in enumerate(level_array):
            for obj_index, obj in enumerate(row):
                position = obj_index * CELL_SIZE, row_index * CELL_SIZE

                if obj: Ground(position)
                else: continue

                switch = {
                    '#': lambda: Stone(position),
                    'M': lambda: Wood(position),
                    'C': lambda: Glass(position),
                    'D': lambda: SmartShooter(position, .3),
                    '$': lambda: Box(position),
                    '.': lambda: True,
                }.get(obj, lambda: None)()

                if not switch:
                    if obj == 'jugador':
                        player_pos = Vector(position) - CENTER + Vector(CELL_SIZE - TANK_FRAME) / 2 + Vector(TANK_FRAME / 2)

                    elif obj:
                        eval(obj)

        try:
            for sprite in level_sprites:
                sprite.rect.topleft -= player_pos
        except UnboundLocalError:
            print('Fin del juego')
            return

        self.walls = pygame.sprite.Group(blocks, shooters, smart_shooters)
        sprite_groups_list.append(self.walls)
        

if __name__ == '__main__':
    Game().mainloop()
