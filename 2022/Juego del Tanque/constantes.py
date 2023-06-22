from pygame.constants import *
from pygame.sprite import Group as G
import pygame

#-------------------Grupos de sprites
# Grupos de los niveles
level_sprites = G()
ground = G()
blocks = G()
shooters = G()
smart_shooters = G()
bullets = G()
boxes_content = G()
enemy_bullets = G()
animations = G()
#los sprites se dibujarán en el orden que aparecen en sprite_groups_list
sprite_groups_list = [ground,
                       bullets,
                       enemy_bullets,
                       boxes_content,
                       blocks,
                       shooters,
                       smart_shooters,
                       animations,
                       ]

#-------------------Medidas
WIDTH = 1024
HEIGHT = 612
CENTER = pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)
CELL_SIZE = 64
TANK_FRAME = CELL_SIZE // 8
ROTARY = 6 #multiplicar CELL_SIZE por esta variable
           #al cambiar el tamaño de una imágen 
           #que tiene que rotar (por ejemplo TANK_CANNON).
FPS = 30

#-------------------Colores
BG = 20,20,20
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GRAY = 80, 80, 80
GREEN = 0, 255, 0
RED = 255, 0, 0
BLUE = 50, 180, 255
BROWN = 190, 130, 100

#-------------------Eventos de teclado
UP = K_w, K_UP
DOWN = K_s, K_DOWN
RIGHT = K_d, K_RIGHT
LEFT = K_a, K_LEFT

#-------------------Otros
FONT_NAME = 'assets/fuente.ttf'

#-------------------Imágenes
from funciones import load_img

TANK_BASE = load_img('tanque/base')
TANK_CANNON = load_img('tanque/cañón')
WEAPON_SIGHT = load_img('tanque/mira', WHITE)
BULLET = load_img('círculo gris')
STONE = load_img('bloques/piedra')
WOOD = load_img('bloques/madera')
GLASS = load_img('bloques/cristal')
GLASS.set_alpha(100)
GROUND = load_img('bloques/suelo')
BOX = load_img('bloques/caja')
MEDICINE_BOX = load_img('botiquín', WHITE)
AMMO_BOX = load_img('tanque/munición', WHITE)
SHOOTER_BASE = BULLET
SHOOTER_CANNON = load_img('disparador cañón')
PLAY_BUTTON = {'normal': load_img('botones/jugar/normal'),
               'mouse over': load_img('botones/jugar/mouse por encima'),
               'pressed': load_img('botones/jugar/presionado')}
EXPLOSION = [load_img(f'explosión/{i}', WHITE) for i in range(1, 8+1)]
SMOKE = [load_img(f'humo/{i}', None) for i in range(6)]
CURTAIN = pygame.Surface((WIDTH, HEIGHT))
CURTAIN.set_alpha(100)
