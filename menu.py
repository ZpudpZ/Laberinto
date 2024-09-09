def update(self):
    self.draw()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        self.selected = (self.selected + 1) % len(self.options)
    elif keys[pygame.K_UP]:
        self.selected = (self.selected - 1) % len(self.options)
    elif keys[pygame.K_RETURN]:
        self.is_active = False
