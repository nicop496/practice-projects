from pygame.font import SysFont
from pygame import Color


def display_text(window, msg, size, center, italic=False, bold=False, color="black"):
    font = SysFont("Serif", size, bold=bold, italic=italic)
    text = font.render(msg, 0, Color(color))
    rect = text.get_rect()
    rect.center = center
    window.blit(text, rect)
    return text