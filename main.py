import pygame
import sys
from nivel import Nivel
from personaje import Personaje
from victoria import Victoria
from amplitud import buscar_amplitud
from profundidad import buscar_profundidad

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
pantalla_ancho = 800
pantalla_alto = 600
pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_alto))
pygame.display.set_caption("Juego de Laberinto")

# Tamaño de las celdas
num_celdas_x = 20
num_celdas_y = 15
tamano_celda_x = pantalla_ancho // num_celdas_x
tamano_celda_y = pantalla_alto // num_celdas_y

# Definir los botones
boton_dfs_rect = pygame.Rect(10, 10, 150, 50)
boton_bfs_rect = pygame.Rect(10, 70, 150, 50)

# Cargar imágenes de fondo
menu_fondo_image = pygame.image.load('assets/menu.png').convert()
pygame.mixer.init()  # Inicializa el mezclador de audio
pygame.mixer.music.load('assets/musica_fondo.mp3')  # Carga el archivo de música
pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen (opcional)
pygame.mixer.music.play(-1)  # Reproduce la música en bucle infinito

def mostrar_menu():
    font = pygame.font.SysFont(None, 74)
    texto_menu = font.render("Menú Principal", True, (255, 255, 255))
    texto_jugar = pygame.font.SysFont(None, 48).render("Presiona ENTER para Jugar", True, (255, 255, 255))

    while True:
        pantalla.blit(menu_fondo_image, (0, 0))  # Dibujar el fondo del menú
        pantalla.blit(texto_menu, (
            pantalla_ancho // 2 - texto_menu.get_width() // 2, pantalla_alto // 2 - texto_menu.get_height() // 2 - 50))
        pantalla.blit(texto_jugar, (
            pantalla_ancho // 2 - texto_jugar.get_width() // 2, pantalla_alto // 2 - texto_jugar.get_height() // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def juego(nivel_numero):
    # Inicializar nivel y personaje
    nivel_archivo = f'niveles/laberinto{nivel_numero}.txt'
    nivel = Nivel(nivel_archivo, tamano_celda_x, tamano_celda_y)
    personaje = Personaje()
    personaje.rect.x = nivel.inicio[0]
    personaje.rect.y = nivel.inicio[1]
    personaje.prev_x, personaje.prev_y = personaje.rect.x, personaje.rect.y

    reloj = pygame.time.Clock()
    victoria = False
    resolver = None  # None, 'dfs', or 'bfs'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_dfs_rect.collidepoint(event.pos):
                    resolver = 'dfs'
                elif boton_bfs_rect.collidepoint(event.pos):
                    resolver = 'bfs'

        if resolver:
            # Ejecutar el algoritmo de búsqueda
            if resolver == 'dfs':
                camino = buscar_profundidad(nivel.obtener_laberinto(), nivel.inicio, nivel.meta)
            elif resolver == 'bfs':
                camino = buscar_amplitud(nivel.obtener_laberinto(), nivel.inicio, nivel.meta)

            # Mover el personaje a lo largo del camino
            for (x, y) in camino:
                personaje.rect.x, personaje.rect.y = x * tamano_celda_x, y * tamano_celda_y
                pantalla.fill((0, 0, 0))
                nivel.draw(pantalla)
                pantalla.blit(personaje.image, personaje.rect)
                pygame.display.flip()
                pygame.time.wait(200)  # Ajusta el tiempo según sea necesario

            if nivel.verificar_victoria(personaje):
                victoria = True
                resolver = None  # Desactivar el modo automático después de la victoria

        else:
            # Lógica normal de movimiento del personaje
            keys = pygame.key.get_pressed()
            movimiento_x = 0
            movimiento_y = 0

            if keys[pygame.K_LEFT]:
                movimiento_x = -5
                personaje.set_state('mover1')
            elif keys[pygame.K_RIGHT]:
                movimiento_x = 5
                personaje.set_state('mover2')
            elif keys[pygame.K_UP]:
                movimiento_y = -5
                personaje.set_state('mover1')
            elif keys[pygame.K_DOWN]:
                movimiento_y = 5
                personaje.set_state('mover2')
            else:
                personaje.set_state('idle')

            personaje.prev_x, personaje.prev_y = personaje.rect.x, personaje.rect.y
            personaje.rect.x += movimiento_x
            personaje.rect.y += movimiento_y

            for muro in nivel.muros:
                if personaje.rect.colliderect(muro):
                    personaje.rect.x = personaje.prev_x
                    personaje.rect.y = personaje.prev_y
                    break

            if nivel.verificar_victoria(personaje):
                victoria = True

            personaje.update()

        pantalla.fill((0, 0, 0))
        nivel.draw(pantalla)
        pantalla.blit(personaje.image, personaje.rect)

        # Dibujar botones
        pygame.draw.rect(pantalla, (0, 255, 0), boton_dfs_rect)
        pygame.draw.rect(pantalla, (0, 0, 255), boton_bfs_rect)
        font = pygame.font.SysFont(None, 36)
        texto_dfs = font.render("DFS", True, (255, 255, 255))
        texto_bfs = font.render("BFS", True, (255, 255, 255))
        pantalla.blit(texto_dfs, (boton_dfs_rect.x + 20, boton_dfs_rect.y + 10))
        pantalla.blit(texto_bfs, (boton_bfs_rect.x + 20, boton_bfs_rect.y + 10))

        if victoria:
            victoria_screen = Victoria(pantalla)
            victoria_screen.draw()
            pygame.display.flip()
            victoria_screen.esperar_continuar()
            return True

        pygame.display.flip()
        reloj.tick(60)

# Ejecutar el juego
nivel_actual = 1
max_niveles = 5

while True:
    mostrar_menu()
    if not juego(nivel_actual):
        break
    nivel_actual += 1
    if nivel_actual > max_niveles:
        break

pygame.quit()
