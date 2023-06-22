import pygame
from constantes import WIDTH, HEIGHT, FONT_NAME
from math import atan2, degrees

def get_angle(a, b, c):
    """
    Devuelve el ángulo de b
    """
    angleAB = atan2(a[0] - b[0], b[1] - a[1])
    angleBC = atan2(b[0] - c[0], c[1] - b[1])
    return round((degrees(180 + angleBC - angleAB) - 53) % 360)

def action_is_pressed(list_of_keys):
    """
    'list of keys' es, por ejemplo: 
    [pygame.K_SPACE, pygame.K_RETURN]

    La función devuelve verdadero si 
    al menos 1 evento es verdadero, sino
    devuelve falso.
    """
    return any([pygame.key.get_pressed()[event] for event in list_of_keys])

def draw_text(window, msg, center, size, color, bold=False, italic=False, bgcolor=None):
    font = pygame.font.Font(FONT_NAME, size)
    text = font.render(msg, True, color, bgcolor)
    rect = text.get_rect(center = center)
    window.blit(text, rect.topleft)
    return text

def load_img(filename, colorkey=(0, 0, 0), extension='.png'):
    img = pygame.image.load('assets/imágenes/' + filename + extension)
    if colorkey: img.set_colorkey(colorkey)
    return img

def load_audio(filename, volume=-1, extension='.wav'):
    audio = pygame.mixer.Sound(f'assets/audio/{filename}{extension}')
    audio.set_volume(volume)
    return audio

def is_visible(sprite):
    if all([sprite.rect.right >= 0,
            sprite.rect.left <= WIDTH,
            sprite.rect.bottom >= 0,
            sprite.rect.top <= HEIGHT]):
        return True
    return False

def read_csv(file_path):
    try:
        with open(file_path, 'r') as file:
            for row in file:
                yield row.replace('\n', '').split(';')
    except FileNotFoundError:
        return

    
