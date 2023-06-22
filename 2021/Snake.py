import pygame, random # Importar las librerias que voy a usar

ANCHO, ALTO = 500, 500 # Dimenciones de la pantalla
BLANCO, NEGRO, VERDE, ROJO = (255,255,255), (0,0,0), (39,184,18), (244,0,0) # Colores

pygame.init() # Iniciar pygame
pantalla = pygame.display.set_mode((ANCHO, ALTO))# Definir la pantalla
pygame.display.set_caption('snake')# Cambiar el nombre de la pantalla 

# Algunas variables de la serpiente
pos_x, pos_y = 100, 20
vel_x, vel_y = 20, 0
posiciones = [(pos_x, pos_y, 20, 20), (80,20, 20, 20), (60,20, 20, 20), (40,20, 20, 20), (20,20,20,20)]
largo = 5

# Posicion inicial de la manzana
num1 = random.randrange(0,ANCHO-40,20)
num2 = random.randrange(0,ALTO-40,20)

# Puntos
puntuacion = 0
max_punt = [puntuacion]

def dibujar_todo():
    pantalla.fill(BLANCO) # El fondo blanco
    pygame.draw.rect(pantalla, ROJO, (num1, num2, 20, 20)) # La manzana
    for s in range(1, largo): pygame.draw.rect(pantalla, VERDE, posiciones[-s]) # La serpiente
    pygame.draw.rect(pantalla, (32, 153, 15), (pos_x, pos_y, 20, 20))

def imprimir_texto(mensaje, x, y, tamaño, tipo_de_letra, color, negrita):
    fuente = pygame.font.SysFont(tipo_de_letra, tamaño, negrita)
    texto = fuente.render(mensaje, True, color)

    if x == 'centro': x = ANCHO//2-texto.get_width()//2
    if x == 'izquierda': x = 5
    if x == 'derecha': x = ANCHO-texto.get_width()-5

    if y == 'centro': y = ALTO//2-texto.get_height()//2
    if y == 'arriba': y = 5
    if y == 'abajo': y = ALTO-texto.get_height()-5

    pantalla.blit(texto, (x, y))

#/#/#/#/#/# Bucle principal /#/#/#/#/#/#
terminado = False
game_over = False
while not terminado:
    # Terminar el bucle principalb
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: terminado = True

    # Movimiento con las flechas del teclado
    teclas = pygame.key.get_pressed()
    if not teclas[pygame.K_DOWN] and not teclas[pygame.K_UP] and vel_y != 0:
        if teclas[pygame.K_RIGHT]: vel_x, vel_y = 20, 0
        if teclas[pygame.K_LEFT]: vel_x, vel_y = -20, 0
    if not teclas[pygame.K_RIGHT] and not teclas[pygame.K_LEFT] and vel_x != 0:
        if teclas[pygame.K_DOWN]: vel_x, vel_y = 0, 20
        if teclas[pygame.K_UP]: vel_x, vel_y = 0, -20

    # Redefinir la posicion de la serpiente
    pos_x += vel_x
    pos_y += vel_y
    pos = (pos_x, pos_y, 20, 20)
    posiciones.append((pos_x, pos_y, 20, 20))

    # Cuando la serpiente come:
    if pos_x == num1 and pos_y == num2:
        num1, num2 = random.randrange(0,ANCHO-40,20), random.randrange(0,ALTO-40,20)
        largo += 1
        puntuacion += 1
        max_punt.append(puntuacion)
    
    # Game over
    for i in range(2, largo):
       # Si la serpiente se choca con si misma o contra la pared es game over 
       if (pos_x, pos_y) == (posiciones[-i][:2]): game_over = True
       if pos_x>ANCHO or pos_x<0 or pos_y>ALTO or pos_y<0: game_over = True
    if game_over: # y si es game over:
        imprimir_texto('Fin del juego', 'centro', 'centro', 50, 'consolas', NEGRO, True)
        imprimir_texto('Presiona "ENTER" para reiniciar', 'centro', 'arriba', 25, 'consolas', NEGRO, True)
        # Volver a jugar
        if teclas[pygame.K_RETURN]:
            game_over = False
            pos_x, pos_y = 100, 20
            vel_x, vel_y = 20, 0
            posiciones = [(pos_x, pos_y, 20, 20), (80,20, 20, 20), (60,20, 20, 20), (40,20, 20, 20), (20,20,20,20)]
            largo = 5
            num1, num2 = random.randrange(0,ANCHO-40,20), random.randrange(0,ALTO-40,20)
            dibujar_todo()
            puntuacion = 0

    else: dibujar_todo()
    
    # Imprimir los puntos
    imprimir_texto(f'Puntuación: {puntuacion}', 'izquierda', 'abajo', 15, 'consolas', NEGRO, False)
    imprimir_texto(f'Máxima puntuación: {max(max_punt)}', 'derecha', 'abajo', 15, 'consolas', NEGRO, False)
    #---------#
    pygame.time.Clock().tick(10)# Establecer los FPS
    pygame.display.flip() # Actualizar la pantalla
pygame.quit() # Salir cuando termine el bucle principal