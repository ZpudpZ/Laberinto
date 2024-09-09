import pygame

class Nivel:
    def __init__(self, archivo, tamano_celda_x, tamano_celda_y):
        self.tamano_celda_x = tamano_celda_x
        self.tamano_celda_y = tamano_celda_y
        self.muros = []
        self.inicio = None
        self.meta = None

        # Cargar imágenes
        self.fondo_image = pygame.image.load('assets/menu_fondo.png').convert()
        self.muro_image = pygame.image.load('assets/muro.png').convert_alpha()
        self.inicio_image = pygame.image.load('assets/inicio.png').convert_alpha()
        self.meta_image = pygame.image.load('assets/meta.png').convert_alpha()

        try:
            self.cargar_nivel(archivo)
        except FileNotFoundError:
            print(f"Error: El archivo {archivo} no se encuentra.")
            raise
        except ValueError as e:
            print(f"Error: {e}")
            raise

    def cargar_nivel(self, archivo):
        with open(archivo, 'r') as f:
            self.laberinto = [line.strip() for line in f]

        for y, fila in enumerate(self.laberinto):
            for x, celda in enumerate(fila):
                if celda == '#':
                    self.muros.append(pygame.Rect(x * self.tamano_celda_x, y * self.tamano_celda_y,
                                                  self.tamano_celda_x, self.tamano_celda_y))
                elif celda == 'S':
                    self.inicio = (x * self.tamano_celda_x, y * self.tamano_celda_y)
                elif celda == 'E':
                    self.meta = (x * self.tamano_celda_x, y * self.tamano_celda_y)

        if self.inicio is None or self.meta is None:
            raise ValueError("El archivo de nivel debe contener una celda de inicio ('S') y una celda de meta ('E').")

    def obtener_laberinto(self):
        # Convertir el laberinto a una representación adecuada para los algoritmos de búsqueda
        return [[1 if celda == '#' else 0 for celda in fila] for fila in self.laberinto]

    def draw(self, screen):
        # Dibujar el fondo
        screen.blit(self.fondo_image, (0, 0))

        # Dibujar muros
        for muro in self.muros:
            # Ajustar el tamaño de la imagen del muro al tamaño de la celda
            muro_image_resized = pygame.transform.scale(self.muro_image, (self.tamano_celda_x, self.tamano_celda_y))
            screen.blit(muro_image_resized, muro.topleft)

        # Dibujar la imagen de inicio
        if self.inicio:
            inicio_rect = pygame.Rect(self.inicio[0], self.inicio[1], self.tamano_celda_x, self.tamano_celda_y)
            inicio_image_resized = pygame.transform.scale(self.inicio_image, (self.tamano_celda_x, self.tamano_celda_y))
            screen.blit(inicio_image_resized, inicio_rect)

        # Dibujar la imagen de meta
        if self.meta:
            meta_rect = pygame.Rect(self.meta[0], self.meta[1], self.tamano_celda_x, self.tamano_celda_y)
            meta_image_resized = pygame.transform.scale(self.meta_image, (self.tamano_celda_x, self.tamano_celda_y))
            screen.blit(meta_image_resized, meta_rect)

    def verificar_victoria(self, personaje):
        if self.meta:
            meta_rect = pygame.Rect(self.meta[0], self.meta[1], self.tamano_celda_x, self.tamano_celda_y)
            return personaje.rect.colliderect(meta_rect)
        return False
