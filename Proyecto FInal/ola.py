import pygame
from pyswip import Prolog
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana del juego
ANCHO = 600
ALTO = 400
TAM_CELDA = 40
FPS = 30
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mazmorras 2D - Juego")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

# Cargar la imagen de fondo
try:
    fondo_imagen = pygame.image.load("fondo.jpg")
    print("Imagen de fondo cargada correctamente.")
except pygame.error as e:
    print(f"Error al cargar la imagen de fondo: {e}")
    fondo_imagen = None

# Verificar si la imagen está cargada correctamente
if fondo_imagen is not None:
    # Obtener las dimensiones originales de la imagen
    fondo_ancho, fondo_alto = fondo_imagen.get_size()

# Inicializar Prolog
prolog = Prolog()
prolog.consult("juego.pl")  # Cargar el archivo de Prolog

# Consultar Prolog para obtener una posición inicial para el jugador
posicion_inicial = list(prolog.query("posicion(X, Y)"))[0]
player_pos = [posicion_inicial["X"] * TAM_CELDA, posicion_inicial["Y"] * TAM_CELDA]

# Configurar el jugador
player_size = TAM_CELDA
player_speed = 10

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Capturar eventos de teclado
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < ANCHO - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < ALTO - player_size:
        player_pos[1] += player_speed

    # Actualizar la pantalla
    if fondo_imagen is not None:
        ventana.blit(fondo_imagen, (0, 0))
    else:
        ventana.fill(NEGRO)
    pygame.draw.rect(ventana, VERDE, (player_pos[0], player_pos[1], player_size, player_size))
    pygame.display.flip()

    # Controlar la velocidad del juego
    pygame.time.Clock().tick(FPS)