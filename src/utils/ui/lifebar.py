import pygame
from utils import Spritesheet


class Lifebar(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = Spritesheet(
                'assets/HUD/LifeBarMiniUnder.png',
                alpha=True).image_at(0, 0, 18, 4)
        self.image.blit(Spritesheet(
            'assets/HUD/LifeBarMiniProgress.png',
            alpha=True)).image_at(0, 0, 18, 4)
