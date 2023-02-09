import pygame
from utils import Spritesheet


class Lifebar(pygame.sprite.Sprite):
    """ Only for enemies """
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = Spritesheet(
                'assets/HUD/LifeBarMiniUnder.png',
                alpha=True).image_at(0, 0, 18, 4)
        self.image.blit(Spritesheet(
            'assets/HUD/LifeBarMiniProgress.png',
            alpha=True)).image_at(0, 0, 18, 4)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
