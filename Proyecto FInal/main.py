import pygame
from pyswip import Prolog
import sys
import random

# Inicializar Pygame
pygame.init()

# Inicializar el módulo de música de Pygame
pygame.mixer.init()

# Cargar y reproducir la música
try:
    pygame.mixer.music.load("Ariath_Math.wav")
    pygame.mixer.music.play(-1)  # Reproducir en bucle
    print("Música cargada y reproducida correctamente.")
except pygame.error as e:
    print(f"Error al cargar la música: {e}")

# Configuración de la ventana del juego
ANCHO = 512
ALTO = 512
TAM_CELDA = 64
FPS = 30
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mazmorras 2D - Juego")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Cargar la imagen de fondo
try:
    fondo_imagen = pygame.image.load("fondo2.png")
    print("Imagen de fondo cargada correctamente.")
except pygame.error as e:
    print(f"Error al cargar la imagen de fondo: {e}")
    fondo_imagen = None

# Cargar las imágenes de los obstáculos
try:
    obstaculo_imagen = pygame.image.load("obstaculos/02.png")
    obstaculo_imagen = pygame.transform.scale(obstaculo_imagen, (TAM_CELDA, TAM_CELDA))
    lago_imagen = pygame.image.load("obstaculos/water.jpg")
    lago_imagen = pygame.transform.scale(lago_imagen, (TAM_CELDA, TAM_CELDA))
    puente_imagen = pygame.image.load("obstaculos/puente.jpg")
    puente_imagen = pygame.transform.scale(puente_imagen, (TAM_CELDA, TAM_CELDA))
    rocas_imagen = pygame.image.load("obstaculos/09.png")
    rocas_imagen = pygame.transform.scale(rocas_imagen, (TAM_CELDA, TAM_CELDA))
    print("Imágenes de obstáculos cargadas y redimensionadas correctamente.")
except pygame.error as e:
    print(f"Error al cargar las imágenes de obstáculos: {e}")
    obstaculo_imagen = None
    lago_imagen = None
    puente_imagen = None
    rocas_imagen = None

# Función para cargar y redimensionar los sprites del personaje
def cargar_sprites(direccion, tamano):
    return [pygame.transform.scale(pygame.image.load(f"{direccion}/{direccion.split('/')[-1]}_{i}.png"), tamano) for i in range(4)]

# Tamaño del personaje
TAM_PERSONAJE = (64, 64)  # Tamaño deseado para el personaje

sprites = {
    "down": cargar_sprites("sprites/down", TAM_PERSONAJE),
    "down_attack": [pygame.transform.scale(pygame.image.load("sprites/down_attack/attack_down.png"), TAM_PERSONAJE)],
    "down_idle": [pygame.transform.scale(pygame.image.load("sprites/down_idle/idle_down.png"), TAM_PERSONAJE)],
    "left": cargar_sprites("sprites/left", TAM_PERSONAJE),
    "left_attack": [pygame.transform.scale(pygame.image.load("sprites/left_attack/attack_left.png"), TAM_PERSONAJE)],
    "left_idle": [pygame.transform.scale(pygame.image.load("sprites/left_idle/idle_left.png"), TAM_PERSONAJE)],
    "right": cargar_sprites("sprites/right", TAM_PERSONAJE),
    "right_attack": [pygame.transform.scale(pygame.image.load("sprites/right_attack/attack_right.png"), TAM_PERSONAJE)],
    "right_idle": [pygame.transform.scale(pygame.image.load("sprites/right_idle/idle_right.png"), TAM_PERSONAJE)],
    "up": cargar_sprites("sprites/up", TAM_PERSONAJE),
    "up_attack": [pygame.transform.scale(pygame.image.load("sprites/up_attack/attack_up.png"), TAM_PERSONAJE)],
    "up_idle": [pygame.transform.scale(pygame.image.load("sprites/up_idle/idle_up.png"), TAM_PERSONAJE)],
}



# Inicializar Prolog
prolog = Prolog()
prolog.consult("prueba.pl")  # Cargar el archivo de Prolog

# Consultar Prolog para obtener una posición inicial para el jugador y el enemigo
posicion_inicial = list(prolog.query("jugador_posicion(X, Y)"))[0]
player_pos = [posicion_inicial["X"] * TAM_CELDA, posicion_inicial["Y"] * TAM_CELDA]



# Configurar el jugador
player_speed = 8
player_direction = "down"
player_action = "idle"
sprite_index = 0



# Función para verificar si una posición es un camino
def es_camino(x, y):
    consulta = list(prolog.query(f"es_camino({x}, {y})"))
    return len(consulta) > 0



# Función para dibujar el mapa
def dibujar_mapa(camera_x, camera_y):
    mapa = list(prolog.query("mapa(M)"))[0]["M"]
    for y, fila in enumerate(mapa):
        for x, celda in enumerate(fila):
            if celda == 0 and obstaculo_imagen:
                ventana.blit(obstaculo_imagen, (x * TAM_CELDA - camera_x, y * TAM_CELDA - camera_y))
            elif celda == 2 and lago_imagen:
                ventana.blit(lago_imagen, (x * TAM_CELDA - camera_x, y * TAM_CELDA - camera_y))
            elif celda == 44 and puente_imagen:
                ventana.blit(puente_imagen, (x * TAM_CELDA - camera_x, y * TAM_CELDA - camera_y))
            elif celda == 33 and rocas_imagen:
                ventana.blit(rocas_imagen, (x * TAM_CELDA - camera_x, y * TAM_CELDA - camera_y))

# Función para dibujar el fondo en mosaico
def dibujar_fondo(camera_x, camera_y):
    if fondo_imagen:
        for y in range(-fondo_imagen.get_height(), ALTO + fondo_imagen.get_height(), fondo_imagen.get_height()):
            for x in range(-fondo_imagen.get_width(), ANCHO + fondo_imagen.get_width(), fondo_imagen.get_width()):
                ventana.blit(fondo_imagen, (x - camera_x % fondo_imagen.get_width(), y - camera_y % fondo_imagen.get_height()))

# Bucle principal del juego
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Capturar eventos de teclado
    keys = pygame.key.get_pressed()
    nueva_pos = player_pos[:]
    player_action = "idle"
    if keys[pygame.K_LEFT]:
        nueva_pos[0] -= player_speed
        player_direction = "left"
        player_action = "idle"
    if keys[pygame.K_RIGHT]:
        nueva_pos[0] += player_speed
        player_direction = "right"
        player_action = "idle"
    if keys[pygame.K_UP]:
        nueva_pos[1] -= player_speed
        player_direction = "up"
        player_action = "idle"
    if keys[pygame.K_DOWN]:
        nueva_pos[1] += player_speed
        player_direction = "down"
        player_action = "idle"

    # Verificar si la nueva posición es un camino
    x, y = nueva_pos[0] // TAM_CELDA, nueva_pos[1] // TAM_CELDA
    if es_camino(x, y):
        player_pos = nueva_pos

    if keys[pygame.K_SPACE]:
        player_action = "attack"

   
    # Calcular la posición de la cámara
    camera_x = player_pos[0] - ANCHO // 2 + TAM_CELDA // 2
    camera_y = player_pos[1] - ALTO // 2 + TAM_CELDA // 2

    # Actualizar la pantalla
    dibujar_fondo(camera_x, camera_y)
    
    # Dibujar el mapa
    dibujar_mapa(camera_x, camera_y)
    
    # Dibujar el jugador
    sprite_key = f"{player_direction}_{player_action}"
    sprite_list = sprites[sprite_key]
    ventana.blit(sprite_list[sprite_index // 10], (ANCHO // 2 - TAM_PERSONAJE[0] // 2, ALTO // 2 - TAM_PERSONAJE[1] // 2))
    sprite_index = (sprite_index + 1) % (len(sprite_list) * 10)


    
    pygame.display.flip()

    # Controlar la velocidad del juego
    clock.tick(FPS)