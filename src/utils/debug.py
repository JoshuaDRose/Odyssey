""" Used for debugging, as name suggests :) """
import json
import utils
import pygame


# colors = json.load(open('src/colors.json'))
pygame.font.init()

class TextBox(pygame.sprite.Sprite):
    fontPath = pygame.font.match_font('InconsolataLGC Nerd Font')

    def __init__(self, x, y):
        # pygame.font.SysFont takes in arguments of fontpath, size (int)
        self.surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont(TextBox.fontPath, 15)
        sample = "The quick brown fox."
        self.image = pygame.Surface([self.font.render(sample).size()])
        self.rect = pygame.Rect(
                x, y, self.image.get_width(), self.image.get_height())
        pygame.draw.rect(
                self.image,
                pygame.Color("#B0BF1A"),
                self.rect,
                2,
                10)

    def draw(self, text):
        text = self.font.render(
                text,
                True,
                pygame.Color("#EFDECD"))
        self.image.blit(
                self.text,
                self.text.get_width() // 2 - self.rect.width // 2,
                self.text.get_height() // 2 - self.rect.height // 2)
        self.surface.blit(self.image, self.rect)
