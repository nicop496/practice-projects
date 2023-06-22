import pygame

WIDTH = 800
HEIGHT = 600

class Muro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/muro.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y