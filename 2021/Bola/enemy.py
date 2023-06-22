import pygame

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    
    def update(self):
        self.animation()
        self.move()

    def animation(self):
        pass

    def move(self):
        pass