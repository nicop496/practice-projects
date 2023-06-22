import pygame
import random
from player import Bolita
from wall import Muro
from ball import Pelota
from enemy import Enemigo

WIDTH = 800
HEIGHT = 600
GREEN = (35, 200, 70)
WHITE = (255, 255, 255)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('BOLITA')
    clock = pygame.time.Clock()
    

    player = Bolita()

    # enemy_list = pygame.sprite.Group()
    # wall_list = pygame.sprite.Group()
    ball_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group(player)

    done = False
    #/#/#/#/#/#/#/#/-Bucle principal-#/#/#/#/#/#/#/#/
    while not done:
        #--------------------------Logica
        all_sprites_list.update()

        #--------------------------Dibujar
        screen.fill(GREEN)
        all_sprites_list.draw(screen)

        #--------------------------Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(all_sprites_list, ball_list)
        #-------------------#
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()