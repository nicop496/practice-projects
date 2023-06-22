import pygame
from constantes import *
from funciones import *
from clases_secundarias import Bullet


class Tank(pygame.sprite.Sprite):
    # Variables
    rotation = angle = vel_x = vel_y = score = 0
    mouse_pos = 0, 0

    # Constantes
    SPEED = CELL_SIZE // 4
    BULLET_SPEED = SPEED * 2
    ROTATION_SPEED = 9
    TANK_SCALE = CELL_SIZE-TANK_FRAME, CELL_SIZE-TANK_FRAME
    CANNON_SCALE = CELL_SIZE*ROTARY-TANK_FRAME, CELL_SIZE*ROTARY-TANK_FRAME 

    def __init__(self, lifes, ammo):
        super().__init__()
        self.lifes = self.LIFES = lifes
        self.ammo = self.AMMO = ammo
        
        self.base = pygame.transform.scale(TANK_BASE.convert(), self.TANK_SCALE)
        self.cannon = pygame.transform.scale(TANK_CANNON.convert(), self.CANNON_SCALE)
        self.rect = self.base.get_rect()
        self.rect.center = CENTER

        # Cargar Efectos de sonido
        self.HIT = load_audio('golpe')
        self.SHOOT = load_audio('disparo')
        self.GET_AMMO = load_audio('recoger munición', .8)
        self.NO_AMMO = load_audio('sin munición')
        self.GET_MEDICINE = load_audio('recoger botiquín')
        self.GET_MEDICINE_COMPLETE_LIFEBAR = load_audio('recoger botiquín con vida llena')

    def update(self, walls):
        self.rotation %= 360
        self.mouse_pos = pygame.mouse.get_pos()
        self.move_and_collide(walls)
        self.process_keys()
        self.bullets_collisions()
        self.box_objects_collisions()

    def draw(self, window):
        # Base del tanque
        old_base_pos = self.rect.center
        rotated_base = pygame.transform.rotate(self.base, -self.rotation)
        base_rect = rotated_base.get_rect(center=old_base_pos)
        window.blit(rotated_base, (base_rect.x, base_rect.y))

        # Cañón
        self.angle = get_angle((self.rect.centerx, 0), self.rect.center, self.mouse_pos)
        rotated_cannon = pygame.transform.rotate(self.cannon, -self.angle)
        cannon_rect = rotated_cannon.get_rect(center=self.rect.center)
        window.blit(rotated_cannon, (cannon_rect.x, cannon_rect.y))

        # Barra de vida
        pygame.draw.rect(window, GREEN, [10, 10, self.lifes / self.LIFES * 200, 25])
        pygame.draw.rect(window, GRAY, [10, 10, 200, 25], 4)

        # Mira
        window.blit(WEAPON_SIGHT,
                    (self.mouse_pos[0]-WEAPON_SIGHT.get_width() /2,
                     self.mouse_pos[1]-WEAPON_SIGHT.get_height()/2))

        # Munición
        draw_text(window,
                  'Munición: ' + str(self.ammo),
                  (WIDTH-150, 40),
                  30,
                  WHITE,
                  bold=False)

    def move_and_collide(self, collideable_sprites):
        """Mueve con ilusión de una cámara y colisiona con otros objetos"""
        # eje x
        for obj in level_sprites:
            obj.rect.x -= self.vel_x
        colliding_list = pygame.sprite.spritecollide(self, collideable_sprites, False)
        self.__collide_x_axis(colliding_list)

        # eje y
        for obj in level_sprites:
            obj.rect.y -= self.vel_y
        colliding_list = pygame.sprite.spritecollide(self, collideable_sprites, False)
        self.__collide_y_axis(colliding_list)

    def bullets_collisions(self):
        if pygame.sprite.spritecollide(self, enemy_bullets, True):
            self.lifes -= 1
            self.HIT.play()

            if self.lifes < 0:
                return True
            return False
    
    def box_objects_collisions(self):
        for power_up in pygame.sprite.spritecollide(self, boxes_content, True):
            if power_up.what_is == 'MEDICINE_BOX':
                if self.lifes < self.LIFES:
                    self.lifes += power_up.value
                    self.GET_MEDICINE.play()
                else:
                    self.GET_MEDICINE_COMPLETE_LIFEBAR.play()
                
            elif power_up.what_is == 'AMMO_BOX':
                self.ammo += power_up.value
                self.GET_AMMO.play()

    def shoot(self):
        if self.ammo >= 1:
            Bullet(self.rect.center, self.angle, Tank.BULLET_SPEED)
            self.ammo -= 1
            self.SHOOT.play()
        else:
            self.NO_AMMO.play()
    
    def reset(self):
        self.rotation = 180
        self.rect.center = CENTER
        self.lifes = self.LIFES
        self.ammo = self.AMMO

    def process_keys(self):
        """No incluye la acción de disparar"""
        up = action_is_pressed(UP)
        down = action_is_pressed(DOWN)
        right = action_is_pressed(RIGHT)
        left = action_is_pressed(LEFT)

        # Movimieto
        #vertical
        if   up   and not down: self.vel_y = -self.SPEED
        elif down and not up:   self.vel_y = self.SPEED
        else: self.vel_y = 0
        #horizontal
        if   right and not left:  self.vel_x = self.SPEED
        elif left  and not right: self.vel_x = -self.SPEED
        else: self.vel_x = 0

        # Rotación
        #diagonal
        if   up    and right: self.__set_direction(45)
        elif right and down:  self.__set_direction(90  + 45)
        elif down  and left:  self.__set_direction(180 + 45)
        elif left  and up:    self.__set_direction(270 + 45)
        #recta
        elif self.vel_x or self.vel_y:
            if   up:    self.__set_direction(0)
            elif right: self.__set_direction(90)
            elif down:  self.__set_direction(180)
            elif left:  self.__set_direction(270)

    def __set_direction(self, desired_rotation):
        """
        Dependiendo de la rotación deseada, el método se fija
        para que lado rotar y aumenta (derecha) o degrementa (izquierda)
        self.rotation en 1.

        360 <= desired rotation <= 1
        """
        if self.rotation == desired_rotation:
            return
        lenght_left = self.__test_rotation(desired_rotation, -1)
        lenght_right = self.__test_rotation(desired_rotation, 1)
        if lenght_left < lenght_right: 
            self.rotation -= self.ROTATION_SPEED
        else:
            self.rotation += self.ROTATION_SPEED

    def __test_rotation(self, desired_rotation, side):
        """
        Sirve para saber hacia qué lado hay que rotar 
        para que sea de la manera más corta posible.

        360 <= desired rotation <= 1
        side == 1 or side == -1
        """
        test_rotation = self.rotation
        lenght = 0
        while test_rotation != desired_rotation:
            test_rotation += self.ROTATION_SPEED * side
            test_rotation %= 360
            lenght += 1

        return lenght
    
    def __collide_x_axis(self, colliding_list):
        if not colliding_list: return
        for obj in level_sprites: obj.rect.x += self.vel_x
        
        for colliding_obj in colliding_list:
            if self.vel_x > 0:
                self.rect.right = colliding_obj.rect.left
            if self.vel_x < 0:
                self.rect.left = colliding_obj.rect.right

    def __collide_y_axis(self, colliding_list):
        if not colliding_list: return
        for obj in level_sprites: obj.rect.y += self.vel_y

        for colliding_obj in colliding_list:
            if self.vel_y > 0:
                self.rect.bottom = colliding_obj.rect.top
            if self.vel_y < 0:
                self.rect.top = colliding_obj.rect.bottom
