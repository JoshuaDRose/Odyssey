""" Character selection screen """
import os
import sys
import pygame
import json
import utils
from pygame import K_RIGHT, K_LEFT, AUDIO_ALLOW_FREQUENCY_CHANGE, AUDIO_ALLOW_CHANNELS_CHANGE
from pygame import K_UP, K_DOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from loguru import logger

if not pygame.mixer.get_init():
    pygame.mixer.init()

pygame.mixer.music.set_volume(1.0)

image_path = os.path.join('assets/Actor/Characters', 'AllPreview.png')
locations = json.load(open('src/profiles.json'))

class ProfileIcon(pygame.sprite.Sprite):
    def __init__(self, image, x, y, group):
        super().__init__(group)
        self.image: pygame.surface.Surface = image
        self.image = pygame.transform.scale2x(self.image)
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
        self.selectBox.set_colorkey((0, 0, 0));
        self.image.blit(self.selectBox, (0, 0))

    def update(self):
        if self.selected:
            self.selectBox.set_alpha(255)
        else:
            self.selectBox.set_alpha(0)

class SelectionScreen:
    def __init__(self):
        self.image_path = image_path
        # NOTE covers have black bg
        self.spritesheet = utils.Spritesheet(self.image_path)
        self.profile_icons = pygame.sprite.Group()
        self.screen = pygame.display.get_surface()
        self.load_profiles()
        self.running = True

        sfx = 'assets/sfx/Menu'
        self.sound_next = pygame.mixer.Sound(os.path.join(sfx, "Menu2.wav"))
        self.sound_prev = pygame.mixer.Sound(os.path.join(sfx, "Menu3.wav"))
        self.sound_select = pygame.mixer.Sound(os.path.join(sfx, "Menu9.wav"))
        self.sound_init = pygame.mixer.Sound(os.path.join(sfx, "choose_character.wav"))

        self.queue = []

        pygame.mixer.Channel(1).set_volume(.5)
        pygame.mixer.Channel(6).set_volume(.75)
        pygame.mixer.Channel(1).play(self.sound_init)

    def load_profiles(self):
        """
        load profile images and add to profile_icons as sprites.
        """

        # width, height = 38, 40
        # scaled = 76, 80

        x = 0
        for character in locations:
            icon = ProfileIcon(
                    self.spritesheet.image_at((
                        locations[character]['x'],
                        locations[character]['y'],
                        38, 40), (20, 27, 27)), x, 0, self.profile_icons)
            x += 76

        for index, icon in enumerate(self.profile_icons):
            if index <= 1:
                icon.selected = True

    def draw(self):
        self.profile_icons.draw(self.screen)
        for icon in self.profile_icons:
            icon.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_RIGHT:
                    if pygame.mixer.Channel(6).get_busy():
                        pygame.mixer.Channel(6).stop()
                    pygame.mixer.Channel(6).play(self.sound_next)
                if event.type == pygame.K_LEFT:
                    if pygame.mixer.Channel(6).get_busy():
                        pygame.mixer.Channel(6).stop()
                    pygame.mixer.Channel(6).play(self.sound_prev)
