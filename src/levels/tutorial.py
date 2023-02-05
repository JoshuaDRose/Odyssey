import pytmx
import pygame
from loguru import logger


class Tutorial(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.running = False

        # NOTE it is times like these that I wish I was using javascript.
        self.fonts = {
                "header": pygame.font.Font('assets/HUD/Font/NormalFont.ttf', 55),
                "body": pygame.font.Font('assets/HUD/Font/NormalFont.ttf', 40)
                }

        self.text = {
                header: {
                    "text": "Hey there!",
                    "font": self.fonts.get("header")
                    },
                body_a: {
                    "text": "I Noticed this is your first time playing!",
                    "font": self.fonts.get("body")
                    },
                body_b: {
                    "text": "Would you like to do a quick tutorial?",
                    "font": self.fonts.get("body")
                    },
                }

        # self.header = self.font.render(self.header, 1, 

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
