import pygame


class Personaje(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Tamaño deseado del personaje (debe coincidir con el tamaño de los muros)
        tamano_personaje = (40, 40)

        # Cargar imágenes y redimensionar
        self.images_idle = [
            pygame.transform.scale(pygame.image.load('assets/personaje/personaje_idle.png').convert_alpha(),
                                   tamano_personaje)
        ]
        self.images_mover1 = [
            pygame.transform.scale(pygame.image.load('assets/personaje/personaje_mover1.png').convert_alpha(),
                                   tamano_personaje),
            pygame.transform.scale(pygame.image.load('assets/personaje/personaje_mover1_2.png').convert_alpha(),
                                   tamano_personaje)
        ]
        self.images_mover2 = [
            pygame.transform.scale(pygame.image.load('assets/personaje/personaje_mover2.png').convert_alpha(),
                                   tamano_personaje),
            pygame.transform.scale(pygame.image.load('assets/personaje/personaje_mover2_2.png').convert_alpha(),
                                   tamano_personaje)
        ]

        # Inicializar el estado actual
        self.state = 'idle'
        self.image = self.images_idle[0]
        self.rect = self.image.get_rect()
        self.rect.x = 40  # Posición inicial X (ajustar según sea necesario)
        self.rect.y = 40  # Posición inicial Y (ajustar según sea necesario)

        # Configurar el reloj para animaciones
        self.animation_timer = pygame.time.get_ticks()
        self.animation_index = 0

    def update(self):
        # Manejar la animación según el estado
        current_time = pygame.time.get_ticks()

        if self.state == 'idle':
            self.image = self.images_idle[0]
        elif self.state == 'mover1':
            if current_time - self.animation_timer > 200:  # Cambiar cada 200 ms
                self.animation_index = (self.animation_index + 1) % len(self.images_mover1)
                self.image = self.images_mover1[self.animation_index]
                self.animation_timer = current_time
        elif self.state == 'mover2':
            if current_time - self.animation_timer > 200:  # Cambiar cada 200 ms
                self.animation_index = (self.animation_index + 1) % len(self.images_mover2)
                self.image = self.images_mover2[self.animation_index]
                self.animation_timer = current_time

    def set_state(self, state):
        # Cambiar el estado y reiniciar el temporizador de animación
        if self.state != state:
            self.state = state
            self.animation_index = 0
            self.animation_timer = pygame.time.get_ticks()
