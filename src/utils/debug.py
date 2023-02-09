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
        self.screen_width = self.surface.get_width()
        print(self.screen_width)
        self.screen_height = self.surface.get_height()

    def draw(self, text, center=False):
        text = self.font.render(text, True, pygame.Color("#FFFFFF"))
        rect = text.get_rect()
        x = 0
        if center:
            x = rect.width // 2 - self.screen_width // 2
        self.surface.blit(text, (abs(x), self.y))
