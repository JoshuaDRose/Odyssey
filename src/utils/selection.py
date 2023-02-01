""" Character selection screen """
import os
import sys
import pygame
import json
import utils

image_path = os.path.join('assets/Actor/Characters', 'AllPreview.png')
locations = json.load(open('src/profiles.json'))

class ProfileIcon(pygame.sprite.Sprite):
    def __init__(self, image, x, y, group):
        super().__init__(group)
        self.image: pygame.surface.Surface = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.selected = False
        # Box to highlight profile icon
        self.selectBox = pygame.Surface(
                (self.rect.width, self.rect.height))
        pygame.draw.rect(
                self.selectBox,
                (255, 255, 255),
                self.rect,
                3)

class SelectionScreen:
    def __init__(self):
        self.image_path = image_path
        # NOTE covers have black bg
        self.spritesheet = utils.Spritesheet(self.image_path)
        self.profile_icons = pygame.sprite.Group()
        self.screen = pygame.display.get_surface()
        self.load_profiles()
        self.running = True

    def load_profiles(self):
        """
        load profile images and add to profile_icons as sprites.
        """
        # width, height = 38, 40
        x, y = 10, 10
        for character in locations:
            icon = ProfileIcon(
                    self.spritesheet.image_at((
                        locations[character]['x'],
                        locations[character]['y'],
                        38, 40)), x, y, self.profile_icons)
            x += 38
        for icon in self.profile_icons:
            if icon.rect.x == 10:
                icon.selected = True

    def draw(self):
        pass

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
