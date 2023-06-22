import pygame

#constantes
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (176, 176, 176)
CYAN = (0, 128, 128)
CYAN_OSCURO = (0, 64, 64)

ANCHO = 800
ALTO = 600

#----CLASE JUGADOR
class Jugador(pygame.sprite.Sprite):
    nivel = None
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('robot.png')
        self.image.set_colorkey(BLANCO)
        self.rect = self.image.get_rect()

        self.rect.x = ANCHO // 2
        self.rect.y = ALTO // 2
    
    def ir_der (self):
        self.rect.x += 50
        for bloque in self.nivel.lista_bloques:
            for caja in self.nivel.lista_cajas:
                #cajas
                if self.rect.y == caja.rect.y: #Si la coord "Y" de self (el jugador) y de la caja son iguales
                    if self.rect.left == caja.rect.left: #y la parte izquierda del self y de la caja son iguales
                        caja.rect.x += 50 #entonces la caja también se moverá

                #bloques
            if self.rect.left == bloque.rect.left and self.rect.y == bloque.rect.y: #igual que a la caja pero
                self.rect.right = bloque.rect.left #self (jugador) no mueve a la caja sino que no puede avanzar

                #que la caja no avance cuando tiene un bloque en frente
            if caja.rect.left == bloque.rect.left and caja.rect.y == bloque.rect.y:
                caja.rect.right = bloque.rect.left
                if caja.rect.right == bloque.rect.left and self.rect.left == caja.rect.left:
                    self.rect.right = caja.rect.left
    
    def ir_izq (self):
        self.rect.x -= 50
        for bloque in self.nivel.lista_bloques:
            for caja in self.nivel.lista_cajas: 
                if self.rect.right == caja.rect.right and self.rect.y == caja.rect.y: caja.rect.x -= 50

                if self.rect.right == bloque.rect.right and self.rect.y == bloque.rect.y: self.rect.left = bloque.rect.right

            if caja.rect.right == bloque.rect.right and caja.rect.y == bloque.rect.y: 
                caja.rect.left = bloque.rect.right
                if caja.rect.left == bloque.rect.right and self.rect.right == caja.rect.right: 
                    self.rect.left = caja.rect.right
    
    def ir_abajo (self):
        self.rect.y += 50
        for bloque in self.nivel.lista_bloques:
            for caja in self.nivel.lista_cajas:
                if self.rect.top == caja.rect.top and self.rect.x == caja.rect.x: caja.rect.y += 50
            
                if self.rect.top == bloque.rect.top and self.rect.x == bloque.rect.x: self.rect.bottom = bloque.rect.top

            if caja.rect.top == bloque.rect.top and caja.rect.x == bloque.rect.x: 
                caja.rect.bottom = bloque.rect.top
                if caja.rect.bottom == bloque.rect.top and self.rect.top == caja.rect.top: 
                    self.rect.bottom = caja.rect.top
    
    def ir_arriba(self):
        self.rect.y -= 50
        for bloque in self.nivel.lista_bloques:
            for caja in self.nivel.lista_cajas:
                if self.rect.bottom == caja.rect.bottom and self.rect.x == caja.rect.x: caja.rect.y -= 50

                if self.rect.bottom == bloque.rect.bottom and self.rect.x == bloque.rect.x: self.rect.top = bloque.rect.bottom

        if caja.rect.bottom == bloque.rect.bottom and caja.rect.x == bloque.rect.x: 
            caja.rect.top = bloque.rect.bottom
            if caja.rect.top == bloque.rect.bottom and self.rect.bottom == caja.rect.bottom: 
                self.rect.top = caja.rect.bottom


#----CLASE CAJA
class Caja(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('caja.png') 
        self.image.set_colorkey(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        pass

#----CLASE CAJA
class Bloque(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('bloque.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


#----CLASE BASE NIVEL
class Base_nivel(object):
    def __init__(self, jugador):
        #crear
        self.lista_cajas = pygame.sprite.Group()
        self.lista_bloques = pygame.sprite.Group()
        self.jugador = jugador

    def update(self):
        #actualizar
        self.lista_cajas.update()
        self.lista_bloques.update()

    def draw(self, pantalla):
        #dibujar
        pantalla.fill(GRIS)
        self.lista_cajas.draw(pantalla)
        self.lista_bloques.draw(pantalla)

#----CLASE NIVEL
class Nivel(Base_nivel):
    def __init__(self, jugador, bloques, cajas):
        Base_nivel.__init__(self, jugador)

        #crear los bloques
        for a in bloques:
            bloque = Bloque(a[0], a[1])
            bloque.jugador = self.jugador
            self.lista_bloques.add(bloque)

        #crear las cajas
        for b in cajas:
            caja = Caja(b[0], b[1])
            caja.jugador = self.jugador
            self.lista_cajas.add(caja)
        

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/
#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/


def main():
    pygame.init()#iniciar pygame

    reloj = pygame.time.Clock()#reloj

    #pantalla
    dimensiones = [ANCHO, ALTO]
    pantalla = pygame.display.set_mode(dimensiones)
    pygame.display.set_caption('sokoban casero')

    jugador = Jugador()#jugador
    
    #niveles
    cajas = [[500, 500], [300, 300]]
    bloques = [(350, 300)]

    lvl_01 = Nivel(jugador, bloques, cajas)

    indice = 0
    lista_niveles = [lvl_01]
    lista_sprites_activos = pygame.sprite.Group(jugador)
#############################################################
    terminado = False
    while not terminado:
        #nivel actual
        nivel_actual = lista_niveles[indice]
        jugador.nivel = nivel_actual

        #bucle de eventos
        for evento in pygame.event.get():
            #salir
            if evento.type == pygame.QUIT:
                terminado = True

            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)

        #-Mover al jugador, frenarlo cuando haya un bloque y mover las cajas
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    jugador.ir_der()

                if evento.key == pygame.K_LEFT:
                    jugador.ir_izq()

                if evento.key == pygame.K_DOWN:
                    jugador.ir_abajo()

                if evento.key == pygame.K_UP:
                    jugador.ir_arriba()
        
        #limites de la pantalla
        if jugador.rect.right > ANCHO:
            jugador.rect.right = ANCHO

        if jugador.rect.left < 0:
            jugador.rect.left = 0

        if jugador.rect.top < 0:
            jugador.rect.top = 0
        
        if jugador.rect.bottom > ALTO:
            jugador.rect.bottom = ALTO

        #actualizar
        lista_sprites_activos.update()
        nivel_actual.update()
        pygame.display.flip()#(la pantalla)

        #dibujar
        nivel_actual.draw(pantalla)
        for x in range(0, 800, 50):
            pygame.draw.line(pantalla, NEGRO, (x, 0), (x, 600))
        for y in range(0, 600, 50):
            pygame.draw.line(pantalla, NEGRO, (0, y), (800, y))
        lista_sprites_activos.draw(pantalla) 

        #establecer los FPS
        reloj.tick(60)  

    #cuando el bucle termine (o sea cuando le des a cerrar la ventana) se quita pygame 
    pygame.quit()

if __name__ == '__main__':
    main()