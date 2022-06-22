import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((32,32))
        self.rect = self.surface.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()