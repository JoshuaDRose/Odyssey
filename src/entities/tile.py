import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
