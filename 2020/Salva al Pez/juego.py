# El asterisco (*) significa que tengo una parte de lo que estoy haciendo adentro del bucle y otra afuera.

blanco = (255, 255, 255)
negro = (0, 0, 0)

import pygame, random
pygame.init()

#Pantalla
x = 800
y = 400
tamaño = (x, y)
pantalla = pygame.display.set_mode((tamaño))
pygame.display.set_caption('Salva al pez')

#Reloj
tiempo = pygame.time.get_ticks()
reloj = pygame.time.Clock()

#Importar las imágenes y la música
musica = pygame.mixer.Sound('musica.mp3')
sonido = pygame.mixer.music.load('game_over.mp3')

fondo = pygame.image.load('fondo.png').convert()

pezimagen = pygame.image.load('pez.png').convert()
pezimagen.set_colorkey((blanco))

basuraimagen = pygame.image.load('desechos_toxicos2.png').convert()
basuraimagen.set_colorkey((blanco))

mouseimagen = pygame.image.load('ayuda.png').convert()
mouseimagen.set_colorkey((blanco))

#Coordenadas de la basura
basura_coord_list = []
for a in range(1):
    basura_x = random.randint(0, 800)
    basura_y = -100
    basura_coord_list.append([basura_x, basura_y])

#----------------Textos
fuente = pygame.font.Font(None, 40)
fuente2 = pygame.font.Font(None, 120)

texto_final_1 = fuente.render('Perdiste, ',0,(blanco))
texto_final_3 = fuente.render('Click para reiniciar.', 0, (blanco))

texto_puntos = fuente.render('Puntos:',0,(blanco))

texto_titulo = fuente2.render('SALVA AL PEZ',0,(blanco))

texto_comenzar = fuente.render('Haz click  para comenzar',0, (blanco))
#---------------Contadores
#Puntos*
contador = 0

#Basura*
contador_b = 0

#Inmunidad*
contador_i = 0
#---------------------#-----------------------------#-----------------------#-----------------------#
terminado = False
game_over = False
empezar = False
while not terminado:
    #Sacar la ventana
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            terminado = True
        
    #Menú principal        
    if empezar == False:
        #Pantalla de inicio
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(texto_titulo, (120, 50))
        pantalla.blit(texto_comenzar, (225, 350))

        #Música
        musica.play()
        
        #Si haces click el juego empieza
        if evento.type == pygame.MOUSEBUTTONDOWN:
            empezar = True

    #El juego
    if empezar == True:
        #Música
        musica.play()
        
        #Fondo
        pantalla.blit(fondo, (0, 0))

        #Mouse de ayuda
        pantalla.blit(mouseimagen, (0, 0))
        
        #Texto puntuación*
        pantalla.blit(texto_puntos, (675, 0))
        
        #Contador*
        if contador_i >= 1:
            contador += 1
            
        texto_contador = fuente.render(str(contador_i * 10), 0, (blanco))
        pantalla.blit(texto_contador, (700, 50))

        #Texto perdiste*
        texto_final_2 = fuente.render('tu puntuación fue ' + str(contador_i * 10) + '.',0,(blanco))
        
        #Pez
        pygame.mouse.set_visible(0)
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        pez = pantalla.blit(pezimagen, (mouse_x, mouse_y))

        #Basura   
        for coordenada in basura_coord_list:
           basura = pantalla.blit(basuraimagen, (coordenada))
           coordenada[1] += 2.5
           
           if coordenada[1] > 410:
                contador_b += 0.3 #Contador de basura*
                contador_i += 1 #Contador de inmunidad*
                coordenada[1] = basura_y
                
                coordenada[0] = random.randint(0, 800)
                
        coordenada[1] += contador_b
        
        #Colisión entre el pez y la basura, es decir, game over
        if contador_i >= 1 and pez.colliderect(basura):
           pygame.mixer.music.play()
           game_over = True
           coordenada[1] = 0
           coordenada[0] = random.randint(0, 800)
           
        if game_over == True:
            pygame.mouse.set_visible(1)
            coordenada[1] = -206
            contador = contador - 1
            pantalla.blit(fondo, (0, 0))
            pantalla.blit(texto_final_1, (250, 100))
            pantalla.blit(texto_final_2, (250, 150))
            pantalla.blit(texto_final_3, (250, 200))
        
            if evento.type == pygame.MOUSEBUTTONDOWN:
                game_over = False
                pygame.mouse.set_visible(0)
                contador_b = 0
                contador_i = 0
                
                if coordenada[1] > 410:
                    contador_i += 1
                
                contador = 0
                contador += 1
                
                coordenada[1] += 2.5
                coordenada[0] = random.randint(0, 800)

    reloj.tick(60) 
    pygame.display.flip()
pygame.quit()
