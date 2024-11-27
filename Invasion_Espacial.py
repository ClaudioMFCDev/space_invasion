import math
import pygame
import random
from pygame import mixer
import io


# String to byte
def fuente_bytes(fuente):
    # Abre el archivo TFF en modo lectura binaria
    with open(fuente, 'rb') as f:
        # lee todos los bytes del archivo y los almacena en una variable
        ttf_bytes = f.read()
    # Crea un objeto ByteIo a partir de los bytes del archivo TFF
    return io.BytesIO(ttf_bytes)



# Inicializamos Pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption('Invasión Espacial')
icono = pygame.image.load('alien.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('fondo3.png')
fuente_como_bytes = fuente_bytes('QuirkyRobot.ttf')
fuente = pygame.font.Font(fuente_como_bytes, 32)
texto_x = 10
texto_y = 10

# Agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# Texto final del juego
fuente_final = pygame.font.Font(fuente_como_bytes, 100)


def texto_final():
    fuente = pygame.font.Font('freesansbold.ttf', 64)
    texto = fuente.render("JUEGO TERMINADO", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(400, 300))  # Centrar el texto en (400, 300)
    pantalla.blit(texto, texto_rect)  # Dibujar el texto en la pantalla



# Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Variable del jugador
img_jugador = pygame.image.load('rocket.png')
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# Variable del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('enemigo.png'))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# Variable de la bala
balas = []
img_bala = pygame.image.load('bala.png')
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 5
bala_visible = False

# Puntaje
puntaje = 0


# Funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# Funcion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# Funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))


# Funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))
    if distancia < 27:
        return True
    else:
        return False


#################
# Loop del juego#
#################
se_ejecuta = True
juego_terminado = False  # Variable para controlar el estado del juego

while se_ejecuta:
    # Imagen de fondo
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        # Evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Si el juego no ha terminado, permite las teclas
        if not juego_terminado:
            # Evento presionar teclas
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugador_x_cambio = -5
                if evento.key == pygame.K_RIGHT:
                    jugador_x_cambio = 5
                if evento.key == pygame.K_SPACE:
                    sonido_bala = mixer.Sound('disparo.mp3')
                    sonido_bala.play()
                    nueva_bala = {
                        "x": jugador_x,
                        "y": jugador_y,
                        "velocidad": -5
                    }
                    balas.append(nueva_bala)

            # Evento soltar teclas
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    jugador_x_cambio = 0

    # Si el juego está terminado, muestra el texto y no procesa más lógica
    if juego_terminado:
        texto_final()
    else:
        # Modificar ubicación del jugador
        jugador_x += jugador_x_cambio

        # Mantener dentro de bordes al jugador
        if jugador_x <= 0:
            jugador_x = 0
        elif jugador_x >= 736:
            jugador_x = 736

        # Movimiento de la bala
        for bala in balas:
            bala["y"] += bala["velocidad"]
            pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
            if bala["y"] < 0:
                balas.remove(bala)

        # Modificar ubicación del enemigo
        for e in range(cantidad_enemigos):
            # Fin del juego
            if enemigo_y[e] > 500:
                for k in range(cantidad_enemigos):
                    enemigo_y[k] = 1000
                juego_terminado = True  # Cambia el estado del juego
                break

            enemigo_x[e] += enemigo_x_cambio[e]

            # Mantener dentro de bordes al enemigo
            if enemigo_x[e] <= 0:
                enemigo_x_cambio[e] = 1
                enemigo_y[e] += enemigo_y_cambio[e]
            elif enemigo_x[e] >= 736:
                enemigo_x_cambio[e] = -1
                enemigo_y[e] += enemigo_y_cambio[e]

            # Colisión
            for bala in balas:
                colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])

                if colision_bala_enemigo:
                    sonido_colision = mixer.Sound('Golpe.mp3')
                    sonido_colision.play()
                    balas.remove(bala)
                    puntaje += 1
                    enemigo_x[e] = random.randint(0, 736)
                    enemigo_y[e] = random.randint(50, 200)
                    break
            # Llamado al enemigo
            enemigo(enemigo_x[e], enemigo_y[e], e)

        jugador(jugador_x, jugador_y)
        mostrar_puntaje(texto_x, texto_y)

    # Actualizar pantalla
    pygame.display.update()
