""" Used for debugging, as name suggests :) """
import math
import json
import utils
import pygame

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
        self.x = x
        self.y = y
        self.image = pygame.Surface((0, 0))
        self.i = 0

    def draw(self, text, time):
        text = self.font.render(text, True, pygame.Color("#EFDECD"))
        rect = text.get_rect()
        self.surface.blit(text,
                (self.surface.get_width() // 2 - rect.width // 2,
                (self.surface.get_height() // 2 - rect.height // 2) + int(math.sin(time * 5) * 2)))
