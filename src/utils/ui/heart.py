import pygame


class Heart(pygame.sprite.Sprite):
    count = 0
    def __init__(self, image, x, y, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        Heart.count += 1
