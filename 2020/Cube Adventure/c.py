import pygame

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (176, 176, 176)

ANCHO = 800
ALTO = 600

#----CLASE JUGADOR
pygame.mixer.init()
pygame.mixer.music.load('cosas\Mi Audio.mp3')
class Jugador(pygame.sprite.Sprite):
    speed_x, speed_y = 0, 0
    nivel = None

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('cosas\cubo.png')
        self.rect = self.image.get_rect()
        
        self.rect.x = 340
        self.rect.y = 530

        self.vidas = 999

    def update(self):
        self.calc_grav()

        #sumarle la velocidad a la coordenada
        self.rect.x += self.speed_x

        #detectar los choques con los bloques por los lados
        bloques_hit_list = pygame.sprite.spritecollide(self, self.nivel.lista_plataformas, False)
        for bloque in bloques_hit_list:
            if self.speed_x > 0:
                self.rect.right = bloque.rect.left
            elif self.speed_x < 0:
                self.rect.left = bloque.rect.right

        self.rect.y += self.speed_y

        #detectar los choques con los bloques por arriba y abajo        
        bloques_hit_list = pygame.sprite.spritecollide(self, self.nivel.lista_plataformas , False) 
        for bloque in bloques_hit_list:
            if self.speed_y > 0:
                self.rect.bottom = bloque.rect.top
            elif self.speed_y < 0:
                self.rect.top = bloque.rect.bottom
 
            self.speed_y = 0  

    def calc_grav(self):
        #calcular la gravedad
        if self.speed_y == 0:
            self.speed_y = 1
        else:
            self.speed_y += 0.35

        #¿está o no en el suelo?
        if self.rect.y >= ALTO - self.rect.height and self.speed_y >= 0:
            self.speed_y = 0
            self.rect.y = ALTO - self.rect.height


    #--Movimiento
    def saltar(self):
        pygame.mixer.music.play()
        self.rect.y += 2
        bloques_hit_list = pygame.sprite.spritecollide(self, self.nivel.lista_plataformas, False)
        self.rect.y -= 2

        if len(bloques_hit_list) > 0 or self.rect.bottom >= ALTO:
            self.speed_y = -11.55

    def ir_der(self):
        self.speed_x = 6

    def ir_izq(self):
        self.speed_x = -6

    def stop(self):
        self.speed_x = 0



#----CLASE PLATAFORMA
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('cosas\ladrillo.png') 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


#----CLASE PINCHO
class Pincho(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        if tipo == 1:
            self.image = pygame.image.load('cosas\pincho.png')
        if tipo == 2:
            self.image = pygame.image.load('cosas\pincho derecha.png')
        if tipo == 3:
            self.image = pygame.image.load('cosas\pincho izquierda.png')
        if tipo == 4:
            self.image = pygame.image.load('cosas\pincho al reves.png')

        self.image.set_colorkey((BLANCO))
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y


#----CLASE PORTAL
class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('cosas\portal.png')
        self.image.set_colorkey((BLANCO))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#----CLASE BOLA
class Bola(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion, limite):
        super().__init__()
        self.image = pygame.image.load('cosas\pelota.png')
        self.image.set_colorkey((BLANCO))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.limite = limite
        self.direccion = direccion
        self.x = x
        self.y = y
    
    def update(self):
        if self.direccion == 0:
            self.rect.x += 1
        elif self.direccion == 1:
            self.rect.y += 1
        elif self.direccion == 2:
            self.rect.x -= 1
        elif self.direccion == 3:
            self.rect.y -= 1
        
        if self.rect.y == self.limite or self.rect.x == self.limite:
            self.rect.x = self.x
            self.rect.y = self.y


#----CLASE BASE NIVEL
class Base_nivel(object):
        def __init__(self, jugador):
            self.lista_plataformas = pygame.sprite.Group()
            self.lista_enemigos = pygame.sprite.Group()
            self.lista_portal = pygame.sprite.Group()
            self.jugador = jugador

        def update(self):
            self.lista_plataformas.update()
            self.lista_enemigos.update()
            self.lista_portal.update()

        def draw(self, pantalla):
            pantalla.fill(GRIS)

            self.lista_enemigos.draw(pantalla)
            self.lista_plataformas.draw(pantalla)
            self.lista_portal.draw(pantalla)

#----CLASE NIVEL
class Nivel(Base_nivel):
    def __init__(self, jugador, bloques, pinchos, portal, x, y, bolas):
        Base_nivel.__init__(self, jugador)
        #crear cada pincho
        for enemigo in pinchos:
            pincho = Pincho(enemigo[0], enemigo[1],enemigo[2])
            pincho.jugador = self.jugador
            self.lista_enemigos.add(pincho)
            
        #crear cada bloque
        for plataforma in bloques:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.jugador = self.jugador
            self.lista_plataformas.add(bloque)
            
        #crear cada bola
        for pelota in bolas:
            bola = Bola(pelota[0], pelota[1], pelota[2], pelota[3])
            bola.jugador = self.jugador
            self.lista_enemigos.add(bola)


        #crear el portal
        portal = portal
        portal.jugador = self.jugador
        self.lista_portal.add(portal)

        self.x = x
        self.y = y

    def update(self):
        pincho_hit_list = pygame.sprite.spritecollide(self.jugador, self.lista_enemigos,  False)
        for i in pincho_hit_list:
            self.jugador.rect.x = self.x
            self.jugador.rect.y = self.y
            self.jugador.vidas -= 1
        self.lista_enemigos.update()
