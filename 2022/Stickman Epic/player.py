import pygame

WITDH = 800
HEIGHT = 600

class Player (pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        #Cargar las imagenes
        self.images_list = []
        for file in range(6): 
            self.images_list.append(pygame.image.load(f'assets/{file}.png'))

        self.blink = [pygame.image.load('assets/Idle.png'),
                      pygame.image.load('assets/blink0.png'),
                      pygame.image.load('assets/blink1.png'),
                      ]

        self.image = pygame.image.load('assets/Idle.png')

        #Obtener el rectangulo de la imagen
        self.rect = self.image.get_rect()
        #Definir la posicion inicial
        self.rect.x = 130
        self.rect.y = 20

        #Definir unas cuantas variables que van a servir luego
        self.speed_x = 0
        self.speed_y = 0

        self.count = 0

        self.index = 0
        self.change_time = 10

        self.index_blink = 0
        self.change_time_blink = 25
        self.timer = 0
    
    def update(self, screen, blocks, right, left, jump):
        self.image.set_colorkey((255,255,255))
        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.collisions(blocks)
        self.move(right, left, jump)
        self.animation()
    
    def collisions(self, blocks):
        self.blocks = blocks
        #Calcular la gravedad
        self.calc_grav()

        # - - - Detectar las colisiones con los rectangulos
        #---Horizontalmente
        #saber si lo que hay que mover es el jugador o la "cámara"
        if any((
            self.rect.x < 400 and self.rect.x > 200,
            self.rect.x >= 400 and self.speed_x < 0 and self.rect.x > 100,
            self.rect.x >= 200 and self.speed_x > 0  and self.rect.x < 400,
            self.rect.x < 200 and self.speed_x > 0)):

            self.rect.x += self.speed_x
            
        else:
            for block in self.blocks:
                block.rect.x -= self.speed_x
        

        blocks_hit_list = pygame.sprite.spritecollide(self, self.blocks, False)
        for block in blocks_hit_list:
            if self.speed_x > 0: self.rect.right = block.rect.left
            if self.speed_x < 0: self.rect.left = block.rect.right

        #---Verticalmente
        self.rect.y += self.speed_y

        blocks_hit_list = pygame.sprite.spritecollide(self, self.blocks, False)
        for block in blocks_hit_list:
            if self.speed_y > 0: self.rect.bottom = block.rect.top
            if self.speed_y < 0: self.rect.top = block.rect.bottom

            self.speed_y = 0
    
    def move(self, right, left, jump):
        # - - - Detección de las teclas presionadas y qué hacer
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[right]:  self.speed_x = 5
        elif keys_pressed[left]:  self.speed_x = -5
        else: self.speed_x = 0

        if keys_pressed[jump]: self.jump()

    def animation(self):
        moving = self.speed_x != 0 or self.speed_y != 0
        # - - - Velocidad de cambio de las imagenes
        self.count += 1
        #de movimiento
        if self.count >= self.change_time and self.speed_x != 0: 
            self.index += 1
            self.count = 0

        if self.index >= len(self.images_list): self.index = 0

        #de pestañar
        if self.count >= self.change_time_blink:
            self.index_blink += 1
            self.count = 0

        if moving: self.index_blink = 0
        if self.index_blink >= len(self.blink): self.index_blink = 0
        
        # - - - Cambio de imágenes
        #Movimiento
        if self.speed_x > 0:    #hacia la derecha
            self.image = self.images_list[self.index]
        elif self.speed_x < 0:  #hacia la izquierda
            self.image = pygame.transform.flip(self.images_list[self.index], True, False)
        elif self.speed_y != 0: #saltando
            self.image = pygame.image.load('assets/jump.png')
        else:                   #quieto
            self.image = pygame.image.load('assets/Idle.png')

        #Pestañar
        #la variable wait es el tiempo que hay que 
        #esperar para pestañar una vez que te quedas quieto
        wait = (self.change_time_blink*len(self.blink)+1)*3

        self.timer += 1
        if self.timer >= wait or moving: 
            self.timer = 0
        
        if not moving and self.timer >= wait - 60:#si no te estas moviendo y esperase lo suficiente:
            self.image = self.blink[self.index_blink]

    def calc_grav(self):
        # Calcular la gravedad
        if self.speed_y == 0: 
            self.speed_y = 1
        else: 
            self.speed_y += .5
        

        # ¿Está o no en el suelo? Si está, que no caiga más
        if self.rect.bottom >= HEIGHT and self.speed_y >= 0:
            self.rect.bottom = HEIGHT
            self.speed_y = 0
    
    def jump(self):
        self.rect.y += 2
        blocks_hit_list = pygame.sprite.spritecollide(self, self.blocks, False)
        self.rect.y -= 2
        if len(blocks_hit_list) >= 1 or self.rect.bottom >= HEIGHT:
            self.speed_y = -11.55
