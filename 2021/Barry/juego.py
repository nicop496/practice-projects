import pygame #importar pygame

# Constantes
ANCHO, ALTO = 1000, 600
BLANCO, NEGRO = (255, 255, 255), (0,0,0)

# Clase Barry
class Barry(pygame.sprite.Sprite):
    # Algunos atributos
    vel_x, vel_y = 0,0
    pos_x, pos_y = ANCHO//2-112,ALTO//2-185
    fondo_x, fondo_y = 0,0
    indice = 0
    mover = False
    quieto = False    

    # Inicializador
    def __init__(self):
        super().__init__()
        # Lista de imagenes
        self.listaImagenes = [
        pygame.image.load('b1.png'),pygame.image.load('b2.png'),
        pygame.image.load('b3.png'),pygame.image.load('b4.png'),
        pygame.image.load('b5.png'),pygame.image.load('b6.png'),  
        pygame.image.load('b7.png'),pygame.image.load('b8.png'),
        ]
        self.imagen_quieto = pygame.image.load('quieto_der.png')

        # Definir la hitbox del personaje
        self.hitbox = pygame.Surface((112,285))
        self.rect = self.hitbox.get_rect()

    # Actualizar
    def update(self, pantalla, cambio):
        # Cambiar la posicion de la hitbox
        self.rect.x, self.rect.y = self.pos_x, self.pos_y

        # Cambiar la posicion del fondo y/o del personaje
        self.fondo_x -= self.vel_x
        self.fondo_y -= self.vel_y
        
        # Que el indice (de las imagenes) no se pase del limite  
        if self.indice+1 >= len(self.listaImagenes): self.indice = 0

        # Definir la imagen de personaje
        self.image = self.listaImagenes[self.indice]
        self.image = pygame.transform.scale(self.image, (75*3, 95*3))            
        self.image.set_colorkey(BLANCO)

        # Si te estas moviendo:
        if self.mover:
            # Si te moves a la izquierda que la imagen sea un espejo
            if self.vel_x < 0 or self.imagen_quieto.get_alpha() == 254:
                self.image = pygame.transform.flip(self.image, True, False)

            # Cambiar las imagenes y dibujarlas para hacer una
            # pequeña animacion
            self.indice += cambio
            pantalla.blit(self.image, (int(self.pos_x), int(self.pos_y)))

        # Si estas quieto
        elif self.quieto:
            # Dibujar la imagen de quieto en la pantalla
            self.imagen_quieto = pygame.transform.scale(self.imagen_quieto, (75*3, 95*3))
            self.imagen_quieto.set_colorkey(BLANCO)
            pantalla.blit(self.imagen_quieto,  (int(self.pos_x), int(self.pos_y)))

    # Metodos para cambiar la velocidad
    def ir_der(self):
        self.mover = True
        self.vel_x = 10
    
    def ir_izq(self):
        self.mover = True
        self.vel_x = -10
    
    def ir_arriba(self):
        self.mover = True
        self.vel_y = -10
    
    def ir_abajo(self):
        self.mover = True
        self.vel_y = 10
    
    def stop(self):
        self.mover = False
        self.quieto = True
        self.vel_x = 0
        self.vel_y = 0

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/

def main():
    pygame.init() # Iniciar pygame

    # Definir unas cuantas cosas
    pantalla = pygame.display.set_mode((ANCHO,ALTO))
    pygame.display.set_caption('Barry')

    fondo = pygame.image.load('fondo grande.png')

    barry = Barry()
    cambio = 0

    terminado = False
    reloj = pygame.time.Clock()

    #---BUCLE PRINCIPAL
    while not terminado:
        # Bucle de eventos
        for evento in pygame.event.get():
            # Salir
            if evento.type == pygame.QUIT:
                terminado = True

            # Movimiento
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: terminado = True
                if evento.key == pygame.K_RIGHT: barry.ir_der(); barry.imagen_quieto.set_alpha(255)
                if evento.key == pygame.K_LEFT:  barry.ir_izq()
                if evento.key == pygame.K_UP:    barry.ir_arriba()
                if evento.key == pygame.K_DOWN:  barry.ir_abajo()
            
            if evento.type == pygame.KEYUP:
                barry.stop()
                if evento.key == pygame.K_LEFT:
                    barry.imagen_quieto = pygame.image.load('quieto_izq.png')
                    barry.imagen_quieto.set_alpha(254)
                if evento.key == pygame.K_RIGHT:
                    barry.imagen_quieto = pygame.image.load('quieto_der.png')
                    barry.imagen_quieto.set_alpha(255)
        
        # Definir la velocidad de cambio de las imagenes del personaje  
        cambio += 1
        if cambio > 1:
            cambio = 0

        pantalla.fill(NEGRO)
        pantalla.blit(fondo,(barry.fondo_x, barry.fondo_y)) # Dibujar la imagen de fondo
        barry.update(pantalla, int(cambio)) # Actualizar al personaje
        reloj.tick(32) # Definir los FPS
        pygame.display.update() # Actualizar la pantalla
    pygame.quit() # Salir cuando termine el bucle

if __name__ == '__main__': main() # Llamar a main()
