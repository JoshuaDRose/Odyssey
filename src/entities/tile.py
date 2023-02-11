import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(
            self,
            x,
            y,
            image,
            # properties,
            group):
        super().__init__(group)
        self.image = image
        # self.properties = properties
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, self.rect)
