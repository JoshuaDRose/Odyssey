import pytmx
import pygame
from loguru import logger


class Tutorial(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.running = False

    def load_sprites(self):
        pass

    def draw(self):
        for sprite in self.sprites:
            """
            if hasattr(sprite, rect):
                sprite.draw(self.screen, sprite.rect)
            else:
                # NOTE Not that clean, but handles any errors
                logger.error(f"Sprite: {sprite} does not have rect")
            """

            sprite.draw(self.screen, sprite.rect)
