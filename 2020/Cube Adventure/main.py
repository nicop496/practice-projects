import pygame
import c
import n1, n2, n3, n4, n5

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (176, 176, 176)

ANCHO = 800
ALTO = 600

#-------MAIN()
def main():
    #iniciar pygame
    pygame.init()
    pygame.mixer.init()

    #pantalla
    dimensiones = [ANCHO, ALTO]
    pantalla = pygame.display.set_mode(dimensiones)
    pygame.display.set_caption('CUBE ADVENTURE')

    #crear al jugador
    jugador = c.Jugador()

    #--------crear los niveles
    lvl_01 = c.Nivel(jugador, n1.bloques, n1.pinchos, n1.portal, n1.x, n1.y, n1.bolas)
    lvl_02 = c.Nivel(jugador, n2.bloques, n2.pinchos, n2.portal, n2.x, n2.y, n2.bolas)
    lvl_03 = c.Nivel(jugador, n3.bloques, n3.pinchos, n3.portal, n3.x, n3.y, n3.bolas)
    lvl_04 = c.Nivel(jugador, n4.bloques, n4.pinchos, n4.portal, n4.x, n4.y, n4.bolas)
    lvl_05 = c.Nivel(jugador, n5.bloques, n5.pinchos, n5.portal, n5.x, n5.y, n5.bolas)
    
    lista_niveles = [lvl_01, lvl_02, lvl_03, lvl_04, lvl_05]
    lista_sprites_activos = pygame.sprite.Group(jugador)

    #indice del nivel actual
    index = 0 
    
    #reloj para controlar los FPS
    reloj = pygame.time.Clock()
    
    #algunas imagenes
    cora1 = pygame.image.load('cosas\cora1.png').convert();cora1.set_colorkey(BLANCO)
    cora2 = pygame.image.load('cosas\cora2.png').convert();cora2.set_colorkey(BLANCO)
    cora3 = pygame.image.load('cosas\cora3.png').convert();cora3.set_colorkey(BLANCO)

    pantalla_final = pygame.image.load('cosas\game over.jpg')
    pantalla_inicial = pygame.image.load('cosas\menu.jpg')
    pantalla_ganar = pygame.image.load('cosas\Ganaste.jpg')

    #musica y sonidos
    musica = pygame.mixer.Sound('cosas\musica.mp3')
    musica.set_volume(0.25)

    musica_triste = pygame.mixer.Sound('cosas\musica triste.mp3')
    musica_triste.set_volume(0.25)

    musica_ganar = pygame.mixer.Sound('cosas\sonido ganar.mp3')
    musica_ganar.set_volume(0.25)

    pygame.mixer.music.load('cosas\Mi Audio.mp3')

    ################################################################################
    terminado = False
    ganar = False
    while not terminado:
        #bucle que detecta eventos
        for evento in pygame.event.get():
            #salir de la pantalla
            if evento.type == pygame.QUIT:
                terminado = True

            #mover jugador...
            if evento.type == pygame.KEYDOWN:
                if jugador.vidas < 4:
                    if evento.key == pygame.K_RIGHT:
                        jugador.ir_der()
                    if evento.key == pygame.K_LEFT:
                        jugador.ir_izq()
                    if evento.key == pygame.K_SPACE:
                        jugador.saltar()
                        pygame.mixer.music.play()
                
                #reiniciar cuando perdes a ganas
                if evento.key == pygame.K_r:
                    if jugador.vidas <= 0:
                        jugador.vidas = 3
                        index = 0
                        jugador.rect.x = 340
                        jugador.rect.y = 530
                        musica_triste.stop()
                        musica.play()
                    if ganar:
                        musica_ganar.stop()
                        musica.play()
                        ganar = False
                        jugador.vidas = 3
                        index = 0
                        jugador.rect.x = 340
                        jugador.rect.y = 530

                if evento.key == pygame.K_s and len(lista_niveles) - 1 != index:
                    index += 1
                
                if evento.key == pygame.K_e and jugador.vidas == 999:
                    jugador.vidas = 3
                
            #...
            if evento.type == pygame.KEYUP and jugador.vidas < 4:
                if evento.key == pygame.K_RIGHT and jugador.speed_x > 0 or evento.key == pygame.K_LEFT and jugador.speed_x < 0:
                    jugador.stop()

        
        #--nivel actual
        nivel_actual = lista_niveles[index]
        ultimo_nivel = len(lista_niveles) - 1

        jugador.nivel = nivel_actual
        
        #ganar
        if pygame.sprite.groupcollide(lista_sprites_activos, nivel_actual.lista_portal,  False, False):
            if index != ultimo_nivel:
                index += 1 
            
            else:
                ganar = True
        if ganar:
            pantalla.blit(pantalla_ganar,(0,0))
            musica.stop()
            musica_ganar.play()
        else:
            #actualizar
            lista_sprites_activos.update()
            nivel_actual.update()

            #dibujar
            nivel_actual.draw(pantalla)
            lista_sprites_activos.draw(pantalla) 

            musica.play()  

            #vidas
            if jugador.vidas == 3:
                pantalla.blit(cora3,(650,40))      
            elif jugador.vidas == 2:
                pantalla.blit(cora2,(650,40))
            elif jugador.vidas == 1:
                pantalla.blit(cora1,(650,40))
            elif jugador.vidas <= 0:
                pantalla.blit(pantalla_final,(0,0))
                musica.stop()
                musica_triste.play()
            #menu
            elif jugador.vidas == 999:
                pantalla.blit(pantalla_inicial,(0,0))



        #paredes (de la pantalla)
        if jugador.rect.right > ANCHO:
            jugador.rect.right = ANCHO

        if jugador.rect.left < 0:
            jugador.rect.left = 0

        if jugador.rect.top <= 0:
            jugador.rect.top = 0

        reloj.tick(60)
        pygame.display.flip()
    pygame.quit()
    

if __name__ == '__main__':
    main()
