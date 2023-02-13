import pygame
from utils.spritesheet import Spritesheet


class Heart(pygame.sprite.Sprite):
    count = 0
    x = 4
    def __init__(self, x, y, group):
        super().__init__(group)
        self.screen = pygame.display.get_surface()
        spritesheet = Spritesheet('assets/HUD/Heart.png', alpha=True)
        self.hearts = {
                "100%": spritesheet.image_at((0, 0, 16, 16)),
                "75%": spritesheet.image_at((16, 0, 16, 16)),
                "50%": spritesheet.image_at((32, 0, 16, 16)),
                "25%": spritesheet.image_at((48, 0, 16, 16)),
                "0%": spritesheet.image_at((64, 0, 16, 16)),
                }
        for i in self.hearts:
            self.hearts[i] = pygame.transform.scale_by(self.hearts[i], 2)
            self.hearts[i].set_colorkey((0, 0, 0))
        self.image = self.hearts["100%"]

        # NOTE set rect after image as image is scaled and rect is not.
        self.rect = self.image.get_rect()

        self.rect.x = Heart.x + 3 + x
        self.rect.y = y

        Heart.x += self.rect.width + 3

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)
