import pygame
import os
from loguru import logger

class Button(pygame.sprite.Sprite):
    """ Button, can be used in choice class as well """
    def __init__(self, x, y, image: str, group=None):
        """
            Constructor inherits all sprite methods, draw is overriden unless
            called from an instance of pygame.sprite.Group().draw()
        """
        if group:
            super().__init__(group)
        else:
            super().__init__()
        if not isinstance(image, str):
            logger.critical(f"Image loaded as {type(image)}, needs to be loaded as string")

        self.path = image
        self.text = self.path
        self.image = pygame.image.load(self.path)
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface) -> None:
        """ Draw image to surface at position of rect """
        surface.blit(self.image, self.rect)
