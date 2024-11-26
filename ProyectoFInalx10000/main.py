from pyswip import Prolog
import pygame
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
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

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
    tierra_imagen = pygame.image.load("tierra.jpeg")
    tierra_imagen = pygame.transform.scale(tierra_imagen, (TAM_CELDA, TAM_CELDA))
    npc_imagen = pygame.image.load("npc/19.png")
    npc_imagen = pygame.transform.scale(npc_imagen, (TAM_CELDA, TAM_CELDA))
    objeto_imagen = pygame.image.load("heal.png")
    objeto_imagen = pygame.transform.scale(objeto_imagen, (TAM_CELDA, TAM_CELDA))
    print("Imágenes de obstáculos cargadas y redimensionadas correctamente.")
except pygame.error as e:
    print(f"Error al cargar las imágenes de obstáculos: {e}")
    obstaculo_imagen = None
    lago_imagen = None
    puente_imagen = None
    rocas_imagen = None
    tierra_imagen = None
    npc_imagen = None
    objeto_imagen = None

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

# Cargar los sprites de la lanza para cada dirección
try:
    TAM_LANZA = (32, 32)  # Tamaño deseado para la lanza
    lanza_sprites = {
        "down": pygame.transform.scale(pygame.image.load("lance/down.png"), TAM_LANZA),
        "left": pygame.transform.scale(pygame.image.load("lance/left.png"), TAM_LANZA),
        "right": pygame.transform.scale(pygame.image.load("lance/right.png"), TAM_LANZA),
        "up": pygame.transform.scale(pygame.image.load("lance/up.png"), TAM_LANZA),
    }
    print("Sprites de la lanza cargados correctamente.")
except pygame.error as e:
    print(f"Error al cargar los sprites de la lanza: {e}")
    lanza_sprites = None

# Función para cargar y redimensionar los sprites del enemigo
def cargar_sprites_enemigo(direccion, tamano):
    return [pygame.transform.scale(pygame.image.load(f"{direccion}.png"), tamano)]


# Tamaño del enemigo
TAM_ENEMIGO = (64, 64)  # Tamaño deseado para el enemigo

# Cargar los sprites del enemigo
enemigo_sprites = {
    "down": cargar_sprites_enemigo("monsters/spirit/move/down/down", TAM_ENEMIGO),
    "left": cargar_sprites_enemigo("monsters/spirit/move/left/left", TAM_ENEMIGO),
    "right": cargar_sprites_enemigo("monsters/spirit/move/right/right", TAM_ENEMIGO),
    "up": cargar_sprites_enemigo("monsters/spirit/move/up/up", TAM_ENEMIGO),
}

# Cargar los sprites del segundo enemigo
enemigo2_sprites = {
    "down": cargar_sprites_enemigo("monsters/bamboo/move/down/down", TAM_ENEMIGO),
    "left": cargar_sprites_enemigo("monsters/bamboo/move/left/left", TAM_ENEMIGO),
    "right": cargar_sprites_enemigo("monsters/bamboo/move/right/right", TAM_ENEMIGO),
    "up": cargar_sprites_enemigo("monsters/bamboo/move/up/up", TAM_ENEMIGO),
}


# Inicializar Prolog
prolog = Prolog()
prolog.consult("prueba.pl")  # Cargar el archivo de Prolog

# Definir la posición inicial del enemigo
posicion_inicial_enemigo = list(prolog.query("enemigo_posicion(X, Y)"))[0]
enemigo_pos = [posicion_inicial_enemigo["X"] * TAM_CELDA, posicion_inicial_enemigo["Y"] * TAM_CELDA]
enemigo_direction = "down"
enemigo_sprite_index = 0
velocidad_enemigo = 2 

# Definir la posición inicial del segundo enemigo
posicion_inicial_enemigo2 = list(prolog.query("enemigo2_posicion(X, Y)"))[0]
enemigo2_pos = [posicion_inicial_enemigo2["X"] * TAM_CELDA, posicion_inicial_enemigo2["Y"] * TAM_CELDA]
enemigo2_direction = "down"
enemigo2_sprite_index = 0
enemigo2_vivo = True

# Consultar Prolog para obtener una posición inicial para el jugador 
posicion_inicial = list(prolog.query("jugador_posicion(X, Y)"))[0]
player_pos = [posicion_inicial["X"] * TAM_CELDA, posicion_inicial["Y"] * TAM_CELDA]

# Configurar el jugador
player_speed = 8
player_direction = "down"
player_action = "idle"
sprite_index = 0
player_health = 100  # Vida inicial del jugador

 # Ajusta este valor según sea necesario

# Tiempo del último cambio de dirección del enemigo
ultimo_cambio_direccion = pygame.time.get_ticks()
intervalo_cambio_direccion = 1000


# Función para verificar si una posición es un camino
def es_camino(x, y):
    consulta = list(prolog.query(f"es_camino({x}, {y})"))
    return len(consulta) > 0

# Función para verificar si una posición es un obstáculo
def es_obstaculo(x, y):
    consulta = list(prolog.query(f"es_obstaculo({x}, {y})"))
    return len(consulta) > 0

# Función para verificar si una posición tiene un objeto
def es_objeto(x, y):
    consulta = list(prolog.query(f"es_objeto({x}, {y})"))
    return len(consulta) > 0

def cambiar_direccion_enemigo(direccion_actual):
    direcciones = ["up", "down", "left", "right"]
    return random.choice(direcciones)
    return direccion

#colision de enemigo con jugador
def verificar_colision(rect1, rect2):
    return rect1.colliderect(rect2)



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
            elif celda == 200 and tierra_imagen:
                ventana.blit(tierra_imagen, (x * TAM_CELDA - camera_x, y * TAM_CELDA - camera_y))
            elif celda == 55 and npc_imagen:
                ventana.blit(npc_imagen, (x * TAM_CELDA - camera_x, y * TAM_CELDA - camera_y))


# Función para dibujar el fondo en mosaico
def dibujar_fondo(camera_x, camera_y):
    if fondo_imagen:
        for y in range(-fondo_imagen.get_height(), ALTO + fondo_imagen.get_height(), fondo_imagen.get_height()):
            for x in range(-fondo_imagen.get_width(), ANCHO + fondo_imagen.get_width(), fondo_imagen.get_width()):
                ventana.blit(fondo_imagen, (x - camera_x % fondo_imagen.get_width(), y - camera_y % fondo_imagen.get_height()))

# Función para dibujar la barra de vida
def dibujar_barra_vida(vida):
    largo_barra = 100
    alto_barra = 20
    borde_barra = pygame.Rect(10, 10, largo_barra, alto_barra)
    vida_barra = pygame.Rect(10, 10, largo_barra * (vida / 100), alto_barra)
    pygame.draw.rect(ventana, ROJO, borde_barra)
    pygame.draw.rect(ventana, VERDE, vida_barra)



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

    x, y = nueva_pos[0] // TAM_CELDA, nueva_pos[1] // TAM_CELDA
    if es_camino(x, y) and not es_obstaculo(x, y):
        jugador_rect = pygame.Rect(nueva_pos[0], nueva_pos[1], TAM_PERSONAJE[0], TAM_PERSONAJE[1])
        enemigo2_rect = pygame.Rect(enemigo2_pos[0], enemigo2_pos[1], TAM_ENEMIGO[0], TAM_ENEMIGO[1])
        enemigo_rect = pygame.Rect(enemigo_pos[0], enemigo_pos[1], TAM_ENEMIGO[0], TAM_ENEMIGO[1])
        if not verificar_colision(jugador_rect, enemigo_rect):
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
    
    # Dibujar la lanza si el jugador está atacando
    if player_action == "attack" and lanza_sprites:
        lanza_sprite = lanza_sprites[player_direction]
        if player_direction == "down":
            lanza_pos = (ANCHO // 2 - TAM_LANZA[0] // 2, ALTO // 2 + 30)
        elif player_direction == "left":
            lanza_pos = (ANCHO // 2 - TAM_PERSONAJE[0] - 0, ALTO // 2 - TAM_LANZA[1] // 2 + 13)
        elif player_direction == "right":
            lanza_pos = (ANCHO // 2 + 30, ALTO // 2 - TAM_LANZA[1] // 2 + 13)
        elif player_direction == "up":
            lanza_pos = (ANCHO // 2 - TAM_LANZA[0] // 2, ALTO // 2 - TAM_PERSONAJE[1] + 5)
        ventana.blit(lanza_sprite, lanza_pos)

    # Dibujar la barra de vida
    dibujar_barra_vida(player_health)

    # Cambiar la dirección del enemigo aleatoriamente si ha pasado el intervalo de tiempo
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - ultimo_cambio_direccion > intervalo_cambio_direccion:
        enemigo_direction = cambiar_direccion_enemigo(enemigo_direction)
        ultimo_cambio_direccion = tiempo_actual


    # Movimiento continuo del enemigo
    nueva_pos_enemigo = enemigo_pos[:]
    if enemigo_direction == "up":
        nueva_pos_enemigo[1] -= velocidad_enemigo
    elif enemigo_direction == "down":
        nueva_pos_enemigo[1] += velocidad_enemigo
    elif enemigo_direction == "left":
        nueva_pos_enemigo[0] -= velocidad_enemigo
    elif enemigo_direction == "right":
        nueva_pos_enemigo[0] += velocidad_enemigo

    # Verificar si la nueva posición del enemigo está dentro de los límites del mapa
    if 0 <= nueva_pos_enemigo[0] < ANCHO and 0 <= nueva_pos_enemigo[1] < ALTO:
        x_enemigo, y_enemigo = nueva_pos_enemigo[0] // TAM_CELDA, nueva_pos_enemigo[1] // TAM_CELDA
        if es_camino(x_enemigo, y_enemigo) and not es_obstaculo(x_enemigo, y_enemigo):
        # Verificar colisión entre el jugador y el enemigo
            jugador_rect = pygame.Rect(player_pos[0], player_pos[1], TAM_PERSONAJE[0], TAM_PERSONAJE[1])
            enemigo_rect = pygame.Rect(nueva_pos_enemigo[0], nueva_pos_enemigo[1], TAM_ENEMIGO[0], TAM_ENEMIGO[1])
            if not verificar_colision(jugador_rect, enemigo_rect):
                enemigo_pos = nueva_pos_enemigo
                
# Dibujar el enemigo
    enemigo_sprite_list = enemigo_sprites[enemigo_direction]
    ventana.blit(enemigo_sprite_list[enemigo_sprite_index // 10], (enemigo_pos[0] - camera_x, enemigo_pos[1] - camera_y))
    enemigo_sprite_index = (enemigo_sprite_index + 1) % (len(enemigo_sprite_list) * 10)


    

    sprite_index = (sprite_index + 1) % (len(sprite_list) * 10)

    pygame.display.flip()

# Controlar la velocidad del juego
    clock.tick(FPS)