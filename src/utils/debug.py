""" Used for debugging, as name suggests :) """
import json
import utils
import pygame


# colors = json.load(open('src/colors.json'))
pygame.font.init()

class TextBox(pygame.sprite.Sprite):
    fontPath = pygame.font.match_font('InconsolataLGC Nerd Font')

    def __init__(self, x, y, size):
        self.surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont(TextBox.fontPath, size)
        """
        pygame.draw.rect( # BUG does not scale as text can change in width
                self.image,
                pygame.Color("#B0BF1A"),
                self.rect,
                2,
                10)
        """
        self.image = pygame.Surface((0, 0))
        self.x = x
        self.y = y

    def draw(self, text):
        text = self.font.render( text, True, pygame.Color("#EFDECD"))
        rect = text.get_rect()
        self.surface.blit(
                text,
                (self.surface.get_width() // 2 - rect.width // 2,
                self.surface.get_height() // 2 - rect.height // 2))
