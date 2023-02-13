import pygame
from utils.spritesheet import Spritesheet


class Heart(pygame.sprite.Sprite):
    count = 0
    width = 0
    x = 4
    y = 2 # NOTE only here for actual ui. Not drawn on character screen
          # ALSO: not used in Shuriken.
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

        self.rect.y = y

        self.rect.x = Heart.x + x
        Heart.x += 3
        Heart.width = self.rect.width

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)

    @staticmethod
    def increment_x_axis() -> None:
        """ Increment x axis when iterating through set_health_count """
        Heart.x += Heart.width
