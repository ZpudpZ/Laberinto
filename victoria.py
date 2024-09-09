import pygame

class Victoria:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.fondo = pygame.image.load('assets/victoria_fondo.png').convert()

    def draw(self):
        self.screen.blit(self.fondo, (0, 0))  # Dibujar el fondo de victoria
        text = self.font.render('¡Victoria!', True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))

    def esperar_continuar(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return
