import pygame

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)

class Pelota(pygame.sprite.Sprite):
    def __init__(self, center, speeds):
        super().__init__()
        self.image = pygame.image.load('assets/pelota0.png')
        self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = 3
        self.speed_x = speeds[0]
        self.speed_y = speeds[1]
        self.rebounds = 0
    
    def update(self):
        self.image = pygame.image.load(f'assets/pelota{self.rebounds}.png')
        self.image.set_colorkey(WHITE)

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= WIDTH: 
            self.speed_x *= -1
            self.rebounds += 1
        
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1
            self.rebounds += 1
        
        if self.rebounds > 2:
            self.kill()

        

        
    