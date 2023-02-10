import pygame

_ = pygame.display.set_mode((0, 0), 0, 32)

class Sprite(pygame.sprite.Sprite):
    def __init__(self,
                 image: pygame.surface.Surface,
                 x: int,
                 y: int, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = x, y
