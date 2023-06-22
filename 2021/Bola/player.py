import pygame
from ball import Pelota

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)

class Bolita(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        file_names = (
            ('bolita abajo.png', 'bolita abajo 0.png', 'bolita abajo 1.png'),
            ('bolita arriba.png', 'bolita arriba 0.png', 'bolita arriba 1.png'),
            ('bolita horizontal.png', 'bolita horizontal 0.png', 'bolita horizontal 1.png'),
        )

        self.images_list = []

        for i in range(len(file_names)):
            self.images_list.append([])
            for file in file_names[i]:
                self.images_list[i].append(pygame.transform.scale(pygame.image.load(f'assets/{file}'), (131,113)))
        
        self.image = self.images_list[0][0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.speed_x = 0
        self.speed_y = 0

        self.moving_down = False
        self.moving_up = False
        self.moving_right = False
        self.moving_left = False

        self.index = 0
        self.count = 0

    def update(self):
        self.animation()
        self.move()
    
    def animation(self):
        self.count += 1
        if self.count > 8:
            self.index += 1
            self.count = 0
        if self.index > 2 or not self.speed_x and not self.speed_y:
            self.index = 0

        if self.moving_right:
            self.image = self.images_list[2][self.index]
        if self.moving_left:
            self.image = pygame.transform.flip(self.images_list[2][self.index], True, False)
        if self.moving_down: #or self.speed_y > 0:
            self.image = self.images_list[0][self.index]
        if self.moving_up: #or self.speed_y < 0:
            self.image = self.images_list[1][self.index]

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]: 
            self.speed_y = 5
            self.moving_down = True
            self.moving_up = False
            self.moving_left = False
            self.moving_right = False

        elif keys[pygame.K_UP]:  
            self.speed_y = -5
            self.moving_up = True
            self.moving_left = False
            self.moving_right = False
            self.moving_down = False

        else: 
            self.speed_y = 0

        if keys[pygame.K_RIGHT]: 
            self.speed_x = 5
            self.moving_right = True
            self.moving_up = False
            self.moving_left = False
            self.moving_down = False

        elif keys[pygame.K_LEFT]: 
            self.speed_x = -5
            self.moving_left = True
            self.moving_up = False
            self.moving_right = False
            self.moving_down = False

        else: 
            self.speed_x = 0

    def shoot(self, *groups):
        if self.speed_x or self.speed_y:
            pelota = Pelota(self.rect.center, (self.speed_x, self.speed_y))
            for group in groups:
                group.add(pelota)