import pygame

WITDH = 800
HEIGHT = 600

BLACK = (0, 0, 0)

class Plataform (pygame.sprite.Sprite):
    def __init__ (self, witdh, height, x, y):
        super().__init__()
        self.image = pygame.Surface((witdh, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill(BLACK)