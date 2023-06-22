import pygame
from player import Player
from plataform import Plataform

WITDH = 800
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WITDH, HEIGHT))
    pygame.display.set_caption('StickMan Epic')
    clock = pygame.time.Clock()
    player = Player()
    blocks_list = pygame.sprite.Group(Plataform(50, 50, WITDH//2-50, HEIGHT//2-50))
    
    # - - - Variables de los rectangulos
    #x1 e y1 son el punto de inicio 
    #x2 e y2 son el ancho y el alto
    x1 = 0
    y1 = 0
    #variable que dice si estas dibujando (por eso drawing) el rectangulo
    drawing = False

    #/#/#/#/#/ Bucle principal #/#/#/#/#
    done = False
    while not done:
        #-----------------------------Logica
        mouse_pos = pygame.mouse.get_pos() #posicion del mouse
        mouse_pressed = pygame.mouse.get_pressed(3) #booleanos de los botones del mouse

        #Dibujar el rectangulo mientras mantegas presionado el mouse
        if mouse_pressed[0]: #el 0 (cero) significa el click izquierdo
            drawing = True

        #Dependiendo de la posicion del mouse definir el ancho y alto
        x2 = mouse_pos[0]-x1
        y2 = mouse_pos[1]-y1

        #Borrar rectangulos
        for block in blocks_list:
            #Si el mouse esta encima de algun bloque...
            if block.rect.collidepoint(mouse_pos):
                #...y hace click derecho...
                if mouse_pressed[2]:
                    #...remover el bloque de la lista de todos los bloques.
                    blocks_list.remove(block)

        #-----------------------------Bucle de eventos
        for event in pygame.event.get():
            #Salir
            if event.type == pygame.QUIT:
                done = True
        
        #Crear los rectangulos
            #Si haces click izquierdo definir la posicion de inicio del rectangulo
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #aca digo que tiene que ser el click IZQUIERDO
                    x1 = mouse_pos[0]
                    y1 = mouse_pos[1]
                
            #Si levantas el dedo del click izquierdo entoces que 
            #añadir el rectangulo a la lista de todos los rectangulos (block_list)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: #aca digo que tiene que ser el click IZQUIERDO
                    drawing = False
                    if x2 > 0 and y2 > 0:
                        block = Plataform(x2, y2, x1, y1)
                        blocks_list.add(block)
        
        #-----------------------------Dibujar todo
        #el fondo
        screen.fill(WHITE)
        #el jugador
        player.update(screen, blocks_list, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP)
        #si es que hay alguno dibujandose, el rectangulo que se esta dibujando 
        if drawing: pygame.draw.rect(screen, (35,35,35), (x1, y1, x2, y2))
        #todos los rectangulos/bloques/plataformas
        blocks_list.draw(screen)  
        #-----------------------------#
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()