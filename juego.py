import pygame
import sys
from amplitud import buscar_amplitud
from profundidad import buscar_profundidad

def juego(nivel_numero):
    nivel_archivo = f'laberinto{nivel_numero}.txt'
    nivel = Nivel(nivel_archivo, tamano_celda_x, tamano_celda_y)
    personaje = Personaje()
    personaje.rect.x = nivel.inicio[0]
    personaje.rect.y = nivel.inicio[1]
    personaje.prev_x, personaje.prev_y = personaje.rect.x, personaje.rect.y  # Inicializar prev_x y prev_y

    reloj = pygame.time.Clock()
    victoria = False
    resolver = None  # None, 'dfs', or 'bfs'

    # Definir los botones para resolver el laberinto
    boton_dfs_rect = pygame.Rect(10, 10, 150, 50)
    boton_bfs_rect = pygame.Rect(10, 70, 150, 50)

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

        # Guardar la posición anterior
        personaje.prev_x, personaje.prev_y = personaje.rect.x, personaje.rect.y

        # Mover el personaje
        personaje.rect.x += movimiento_x
        personaje.rect.y += movimiento_y

        # Colisión con muros
        for muro in nivel.muros:
            if personaje.rect.colliderect(muro):
                # Restaurar la posición anterior si hay colisión
                personaje.rect.x = personaje.prev_x
                personaje.rect.y = personaje.prev_y
                break  # Salir del bucle si hay una colisión

        if resolver:
            if resolver == 'dfs':
                camino = buscar_profundidad(nivel.obtener_laberinto(), nivel.inicio, nivel.meta)
            elif resolver == 'bfs':
                camino = buscar_amplitud(nivel.obtener_laberinto(), nivel.inicio, nivel.meta)

            if camino:
                # Mover el personaje a lo largo del camino
                for (x, y) in camino:
                    personaje.rect.x, personaje.rect.y = x * tamano_celda_x, y * tamano_celda_y
                    pantalla.fill((0, 0, 0))
                    nivel.draw(pantalla)
                    pantalla.blit(personaje.image, personaje.rect)
                    pygame.display.flip()
                    pygame.time.wait(200)  # Ajusta el tiempo según sea necesario
                resolver = None  # Desactivar el modo automático después de la victoria

        # Verificar victoria
        if nivel.verificar_victoria(personaje):
            victoria = True

        # Actualizar
        personaje.update()

        # Dibujar
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
            font = pygame.font.SysFont(None, 74)
            texto_victoria = font.render("Victoria!", True, (0, 255, 0))
            pantalla.blit(texto_victoria, (pantalla_ancho // 2 - texto_victoria.get_width() // 2,
                                           pantalla_alto // 2 - texto_victoria.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  # Esperar 2 segundos antes de pasar al siguiente nivel
            return True  # Indicar que se ha ganado el nivel

        pygame.display.flip()
        reloj.tick(60)
