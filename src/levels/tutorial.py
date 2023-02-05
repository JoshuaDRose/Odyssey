import pytmx
import json
import pygame
import pyscroll
from entities import Player, Tile
from utils import Camera
from loguru import logger
from pytmx.util_pygame import load_pygame


TILE_WIDTH = int()
TILE_HEIGHT = int()

logger.info("Reading tile data")
with open('src/data/tiles.json') as fp:
    data = json.load(fp)
    TILE_HEIGHT = data['TILE_HEIGHT']
    TILE_WIDTH = data['TILE_WIDTH']

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

        self.tmx_map = load_pygame(
                "src/data/maps/tutorial.tmx",
                allow_duplicate_names=False)
        self.scrolling_layer = pyscroll.BufferedRenderer(
                pyscroll.TiledMapData(self.tmx_map),
                (400, 400))

        self.sprites = pyscroll.PyscrollGroup(self.scrolling_layer)
        self.player = Player(100, 100, self.sprites)
                
        logger.debug("Reading src/data/maps/tutorial.tmx")
        self.load_sprites()
        logger.debug("Finished generating tutorial sprites")

    def load_sprites(self):
        x = 0
        y = 0
        for layer in self.tmx_map.visible_tile_layers:
            for x, y, image in layer.tiles():
                if y > self.scrolling_layer._size[0]:
                    y += TILE_HEIGHT
                    x = 0
                Tile(x, y, image, self.sprites)
                x += TILE_WIDTH

    def handle_keys(self):
        key = pygame.key.get_pressed()

        self.player.position.x += (key[K_s] - key[K_a]) * self.player.velocity.x * dt
        self.player.position.y += (key[K_r] - key[K_w]) * self.player.velocity.y * dt

    def draw_map(self):
        self.sprites.draw(self.screen)

    def draw_sprites(self):
        """ 
        Draw sprites to surface.
        NOTE: Components of this are taken from https://github.com/bitcraft/pytmx#basic-use
        """
        
        self.sprites.center(self.player.rect.center)
        self.player.update()
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
