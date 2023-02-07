import pygame
from utils.spritesheet import Spritesheet


class Heart(pygame.sprite.Sprite):
    count = 0
    x = 32
    y = 32
    def __init__(self, x, y, group):
        super().__init__(group)
        spritesheet = Spritesheet('assets/HUD/Heart.png', alpha=True)
        self.hearts = {
                "100%": spritesheet.image_at((0, 0, 16, 16)),
                "75%": spritesheet.image_at((16, 0, 16, 16)),
                "50%": spritesheet.image_at((32, 0, 16, 16)),
                "25%": spritesheet.image_at((48, 0, 16, 16)),
                "0%": spritesheet.image_at((64, 0, 16, 16)),
                }
        for i in self.hearts:
            self.hearts[i] = pygame.transform.scale_by(self.hearts[i], 3)
            self.hearts[i].set_colorkey((0, 0, 0))
        self.image = self.hearts["100%"]

        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        Heart.x += self.rect.width
        Heart.count += 1
