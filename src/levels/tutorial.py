import sys
import pytmx
import pyscroll
import pygame
import json
from entities import Player, Tile
from utils import Camera, Spritesheet
from loguru import logger
from pytmx.util_pygame import load_pygame
from pytmx import TiledMap
from pytmx.pytmx import TiledObject, TiledTileLayer

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
        logger.debug(self.screen)
        self.clock = pygame.time.Clock()
        self.running = False

        self.fonts = {
                "header": pygame.font.Font('assets/HUD/Font/NormalFont.ttf', 55),
                "body": pygame.font.Font('assets/HUD/Font/NormalFont.ttf', 30)
                }

        self.do_zoom =0
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

        self.tmx_map = load_pygame("src/data/maps/tutorial.tmx")

        self.player_spawn = self.tmx_map.get_object_by_name('player')
        """
        logger.debug(self.player_spawn.__dir__()) YIELDS:
        properties parent id name type x y width height rotation gid
        visible closed template image parse_xml apply_transformations as_points allow_duplicate_names
         """

        self.scrolling_layer = pyscroll.BufferedRenderer(
                pyscroll.TiledMapData(self.tmx_map),
                (400, 400))

        self.scrolling_layer.zoom = 1.5

        self.sprites = pyscroll.PyscrollGroup(self.scrolling_layer)
        self.player = Player(self.player_spawn.x, self.player_spawn.y, self.sprites)

        self.tutorial_spritesheet = Spritesheet( f'assets/HUD/Tuto.png')
        self.tutorial_move = self.tutorial_spritesheet.image_at((0, 0, 40, 40))
                
        logger.debug("Reading src/data/maps/tutorial.tmx")
        self.load_sprites()
        logger.debug("Finished generating tutorial sprites")

    def load_sprites(self):
        px = 0
        py = 0
        for layer in self.tmx_map.layers:
            if isinstance(layer, TiledTileLayer):
                for x, y, image in layer.tiles():
                    if py > self.scrolling_layer._size[0]:
                        py += TILE_HEIGHT
                        px = 0
                    Tile(px, py, image, self.sprites)
                    px += TILE_WIDTH

    def draw_sprites(self):
        """ 
        Draw sprites to surface.
        NOTE: Components of this are taken from https://github.com/bitcraft/pytmx#basic-use
        """
        self.sprites.center(self.player.rect.center)
        self.sprites.draw(self.screen)

        self.player.hearts.draw(self.screen)

        self.player.handle_keys()
        self.player.update()


        pygame.display.update()
        self.clock.tick(60)
