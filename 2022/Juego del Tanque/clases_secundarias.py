import pygame
from constantes import *
from funciones import load_audio, get_angle
from random import choice, randrange

SpriteGroup = pygame.sprite.Group
Vector = pygame.math.Vector2

class Block(pygame.sprite.Sprite):
    SCALE = CELL_SIZE, CELL_SIZE

    def __init__(self, image, position):
        super().__init__(level_sprites, blocks)
        self.image = pygame.transform.scale(image, self.SCALE)
        self.rect = self.image.get_rect(topleft=position)


class Bullet(pygame.sprite.Sprite):
    SCALE = CELL_SIZE//3, CELL_SIZE//3

    def __init__(self, center, angle, speed):
        super().__init__(level_sprites, bullets)
        self.image = pygame.transform.scale(BULLET.convert(), self.SCALE)
        self.rect = self.image.get_rect(center=center)
        self.velocity = Vector(0, speed).rotate(angle) * -1

    def update(self):
        self.rect.center += self.velocity
        if not pygame.sprite.spritecollideany(self, ground):
            self.kill()


class Shooter(pygame.sprite.Sprite):
    CANNON_SCALE = CELL_SIZE*ROTARY, CELL_SIZE*ROTARY
    BASE_SCALE = CELL_SIZE, CELL_SIZE

    def __init__(self, position, cooldown, angle):
        super().__init__(level_sprites, shooters)
        self.cooldown = cooldown
        self.angle = angle
        self.cannon = pygame.transform.scale(SHOOTER_CANNON.convert(), self.CANNON_SCALE)
        self.base = pygame.transform.scale(SHOOTER_BASE.convert(), self.BASE_SCALE)
        self.rect = self.base.get_rect(topleft=position)
        self.counter = 0
        self.SHOOT = load_audio('disparo', volume=.1)

    def update(self):
        self.counter += 1
        if self.counter / FPS >= self.cooldown:
            self.counter = 0
            bullet = Bullet(self.rect.center, self.angle, CELL_SIZE // 5)
            bullet.add(enemy_bullets)
            self.SHOOT.play()
        
    def draw(self, window):
        rotated_cannon = pygame.transform.rotate(self.cannon, -self.angle)
        rect = rotated_cannon.get_rect(center=self.rect.center)
        window.blit(self.base, self.rect.topleft)
        window.blit(rotated_cannon, rect.topleft)


class SmartShooter(Shooter):
    def __init__(self, position, cooldown):
        super().__init__(position, cooldown, 0)
        self.remove(shooters)
        self.add(smart_shooters)

    def update(self, player_pos):
        super().update()
        self.angle = get_angle((self.rect.centerx, self.rect.centery-100),
                               self.rect.center,
                               player_pos)


class Animation(pygame.sprite.Sprite):
    current_frame = 0
    counter = 0

    def __init__(self, center, animation_frames,  scale = (CELL_SIZE, CELL_SIZE), animation_speed = .1):
        super().__init__(level_sprites, animations)
        self.anim_speed = animation_speed
        self.frames = animation_frames
        self.scale = scale
        self.image = pygame.transform.scale(self.frames[0].convert(), scale)
        self.rect = self.image.get_rect(center = center)
    
    def update(self):
        self.counter += 1
        if self.counter / FPS >= self.anim_speed:
            self.counter = 0
            self.current_frame += 1
            try:
                self.image = pygame.transform.scale(self.frames[self.current_frame].convert(), self.scale)
            except IndexError:
                self.kill()


class BoxContent(pygame.sprite.Sprite):
    SCALE = CELL_SIZE//3*2, CELL_SIZE//3*2

    def __init__(self, position, value, image, what_is):
        super().__init__(level_sprites, boxes_content)
        self.what_is = what_is
        self.value = value
        self.image = pygame.transform.scale(image.convert(), self.SCALE)
        self.rect = self.image.get_rect(topleft=position)


class Wood(Block):
    def __init__(self, position, life_points=4):
        """life_points % CELL_SIZE == 0"""
        super().__init__(WOOD.convert(), position)
        self.life_points = life_points
        self.init_life_points = life_points
        self.BREAK = load_audio('madera se rompe')
        

    def update(self):
        if pygame.sprite.spritecollide(self, bullets, True):
            if self.life_points > 1:
                self.life_points -= 1
            else:
                self.BREAK.play()
                self.kill()

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)
        if self.life_points < self.init_life_points:
            rect = self.rect.bottomleft[0], self.rect.bottomleft[1]-self.lifebar_height, self.rect.width, self.lifebar_height
            pygame.draw.rect(window, GREEN, (rect[0], rect[1], self.life_points * (rect[2] / self.init_life_points), rect[3]))
            pygame.draw.rect(window, BLACK, rect, width=2)
    
    @property
    def lifebar_height(self):
        return self.rect.height / 10


class Box(Wood):
    SCALE = (CELL_SIZE//3*2, CELL_SIZE//3*2)

    def __init__(self, position, life_points=3, content='random'):
        super().__init__(position, life_points)
        self.BREAK = load_audio('caja se rompe')
        self.image = pygame.transform.scale(BOX.convert(), self.SCALE)
        self.rect = self.image.get_rect(x=position[0] + CELL_SIZE / 3 / 2, y=position[1] + CELL_SIZE / 3 / 2)

        self.content = choice([(1, MEDICINE_BOX, 'MEDICINE_BOX'), (10, AMMO_BOX, 'AMMO_BOX')]) if content == 'random' else content

    def update(self):
        if pygame.sprite.spritecollide(self, bullets, True):
            if self.life_points > 1:
                self.life_points -= 1
            else:
                self.BREAK.play()
                x = randrange(self.rect.centerx - 20, self.rect.centerx + 20)
                y = randrange(self.rect.centery - 20, self.rect.centery + 20)
                position = x, y
                BoxContent(position, self.content[0], self.content[1], self.content[2])
                self.kill()


class Ground(Block):
    def __init__(self, position):
        super().__init__(GROUND.convert(), position)
        self.remove(blocks)
        self.add(ground)


class Stone(Block):
    def __init__(self, position):
        super().__init__(STONE.convert(), position)

    def update(self):
        pygame.sprite.spritecollide(self, bullets, True)


class Glass(Block):
    def __init__(self, position):
        super().__init__(GLASS.convert(), position)
        #self.BREAK = load_sound('vidrio se rompe')
        
    def update(self):
        if pygame.sprite.spritecollide(self, bullets, False):
            #self.BREAK.play()
            self.kill()
