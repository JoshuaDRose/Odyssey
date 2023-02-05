import pytmx
import pygame
import pyscroll
from entities import Player
from utils import Camera
from loguru import logger
from pytmx.util_pygame import load_pygame


class Tutorial(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.running = False

        # NOTE it is times like these that I wish I was using javascript.
        self.fonts = {
                "header": pygame.font.Font('assets/HUD/Font/NormalFont.ttf', 55),
                "body": pygame.font.Font('assets/HUD/Font/NormalFont.ttf', 30)
                }

        self.text = {
                'header': {
                    "text": "Hey there!",
                    "font": self.fonts.get("header"),
                    },
                'body_a': {
                    "text": "I Noticed this is your first time playing!",
                    "font": self.fonts.get("body"),
                    },
                'body_b': {
                    "text": "Would you like to do a quick tutorial?",
                    "font": self.fonts.get("body"),
                    },
                }

        for key in self.text:
            self.text[key]["render"] = self.text[key]["font"].render(self.text[key]["text"], 1, (228, 190, 58))
            self.text[key]["rect"] = self.text[key]["render"].get_rect()
            self.text[key]["rect"].x = self.screen.get_width() // 2 - self.text[key]["rect"].width // 2

        self.text["header"]["rect"].y = 100
        self.text["body_a"]["rect"].y = 190
        self.text["body_b"]["rect"].y = 230

        # self.player = str()

        self.tmx_map = load_pygame("src/data/maps/tutorial.tmx")
        self.scrolling_layer = pyscroll.BufferedRenderer(
                pyscroll.TiledMapData(self.tmx_map),
                (400, 400))

        self.sprites = pyscroll.PyscrollGroup(self.scrolling_layer)
        self.player = Player(100, 100, self.sprites)

    def load_sprites(self):
        pass

    def handle_keys(self):
        key = pygame.key.get_pressed()

        self.player.position.x += (key[K_s] - key[K_a]) * self.player.velocity.x * dt
        self.player.position.y += (key[K_r] - key[K_w]) * self.player.velocity.y * dt

    def draw(self):
        """ 
        Draw sprites to surface.
        NOTE: Components of this are taken from https://github.com/bitcraft/pytmx#basic-use
        """
        
        self.sprites.center(self.player.rect.center)
        self.sprites.draw(self.screen)
        pygame.display.update()

        """
        for sprite in self.sprites:
            if hasattr(sprite, rect):
                sprite.draw(self.screen, sprite.rect)
            else:
                # NOTE Not that clean, but handles any errors
                logger.error(f"Sprite: {sprite} does not have rect")

            sprite.draw(self.screen, sprite.rect)
        """
