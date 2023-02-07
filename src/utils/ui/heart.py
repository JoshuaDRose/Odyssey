import pygame


class Heart(pygame.sprite.Sprite):
    count = 0
    x = 15
    y = 15
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = pygame.image.load(f'assets/HUD/Heart.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        Heart.x += self.rect.width
        Heart.count += 1
