import pygame
from display_text import display_text


class Button(pygame.sprite.Sprite):
    def __init__(self, window, position, size, func=None, text='', keep_pressed=False):
        super().__init__()
        self.window = window 
        self.keep = keep_pressed
        self.text = text
        self.func = func
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.rect.topleft = position
        self.mouse_is_over = False
        self.is_pressed = False
        self.color = pygame.Color("black")
    
    def update(self, click_event: bool):
        # Cursor over
        self.mouse_is_over = self.rect.collidepoint(pygame.mouse.get_pos())
        self.color = pygame.Color("blue") if self.is_pressed or self.mouse_is_over else pygame.Color("black")

        # Know if the click is being pressed
        if self.mouse_is_over and click_event:
            self.is_pressed = True
            if self.func:
                self.func()

        elif not self.keep:
            self.is_pressed = False

    def draw(self, size=0, bold=False, italic=False):
        """
        The parameters refers to the text of the button
        """
        pygame.draw.rect(self.window, self.color, self.rect, width=3)

        if self.text:
            display_text(
                self.window,
                self.text, 
                self.rect.width // 3 if not size else size,             
                self.rect.center, 
                italic=italic,
                bold=bold
            )