import pygame


class Piece(pygame.sprite.Sprite):
    def __init__(self,size,x,y,path):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (size,size))
        self.rect = self.image.get_rect(topleft = (x,y))

class Highlight(pygame.sprite.Sprite):
    def __init__(self,tile_size,pos,color):
        super().__init__()
        self.image = pygame.Surface((tile_size,tile_size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = pos)
        