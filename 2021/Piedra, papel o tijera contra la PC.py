import random

def piedra_papel_tijera():
    jugador = input('Elige "piedra", "papel", o "tijera":  ')
    posibles = ('piedra', 'papel', 'tijera')
    maquina = random.choice(posibles)
    m_gana = 0
    j_gana = 0
    
    while True:
        while jugador != 'piedra' and jugador != 'papel' and jugador != 'tijera':
            jugador = input('Elige de nuevo (y bien): ')
            
        if jugador == 'piedra' and maquina == 'tijera' or jugador == 'papel' and maquina == 'piedra' or jugador == 'tijera' and maquina == 'papel':
            j_gana += 1
            marcador = f'\nMáquina {m_gana} - Jugador {j_gana}. Elige de nuevo: '
            if m_gana == 3 or j_gana == 3:
                print(maquina)
                break
            print(maquina)
            jugador = input(marcador)
            maquina = random.choice(posibles)

        elif maquina == 'piedra' and jugador == 'tijera' or maquina == 'papel' and jugador == 'piedra' or maquina == 'tijera' and jugador == 'papel':
            m_gana += 1
            marcador = f'\nMáquina {m_gana} - Jugador {j_gana}. Elige de nuevo: '
            if m_gana == 3 or j_gana == 3:
                print(maquina)
                break
            print(maquina)
            jugador = input(marcador)
            maquina = random.choice(posibles)

        else:
            marcador = f'\nMáquina {m_gana} - Jugador {j_gana}. Elige de nuevo: '
            print(maquina)
            jugador = input(marcador)
            maquina = random.choice(posibles)

    print(f'\n{marcador[0:-18]}. Fin del juego')


pregunta = input('¿Queres jugar al piedra, papel o tijera contra una computadora? (s/n): ')
while True:
    if pregunta == 's':
        piedra_papel_tijera()
        pregunta = input('¿Queres volver a jugar? (s/n): ')
        
    elif pregunta == 'n':
        input('Ok, chau')
        break

    else:
        pregunta = input('Escribí "s" o "n" para decir sí o no respectivamente: ') 
