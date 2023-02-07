""" Character selection screen """
import os
import math
import time
import sys
import pygame
import json
import utils
from .debug import TextBox
from pygame import K_RIGHT, K_LEFT, AUDIO_ALLOW_FREQUENCY_CHANGE, AUDIO_ALLOW_CHANNELS_CHANGE
from loguru import logger

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

if not pygame.mixer.get_init():
    pygame.mixer.init()

pygame.mixer.music.set_volume(0.1)

image_path = os.path.join('assets/Actor/Characters', 'AllPreview.png')
sfx = 'assets/sfx/Menu'

try:
    locations = json.load(open('src/data/profiles.json'))
except FileNotFoundError:
    os.chdir('..')
locations = json.load(open('src/data/profiles.json'))

current_text = ""


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((76, 80), pygame.SRCALPHA)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        pygame.draw.rect(self.image, (255, 255, 255), self.rect, 3)
        self.sound_next = pygame.mixer.Sound(os.path.join(sfx, "Menu2.wav"))
        self.sound_prev = pygame.mixer.Sound(os.path.join(sfx, "Menu3.wav"))
        self.sound_select = pygame.mixer.Sound(os.path.join(sfx, "Menu9.wav"))

    def select(self, character, key=pygame.K_RIGHT):
        global current_text
        select = False
        if key == pygame.K_RIGHT:
            if pygame.mixer.Channel(6).get_busy():
                pygame.mixer.Channel(6).stop()
            pygame.mixer.Channel(6).play(self.sound_next)
        elif key == pygame.K_LEFT:
            if pygame.mixer.Channel(6).get_busy():
                pygame.mixer.Channel(6).stop()
            pygame.mixer.Channel(6).play(self.sound_prev)
        elif key == pygame.K_SPACE:
            if pygame.mixer.Channel(6).get_busy():
                pygame.mixer.Channel(6).stop()
            pygame.mixer.Channel(6).play(self.sound_select)
            select = True
        elif key == pygame.K_RETURN:
            if pygame.mixer.Channel(6).get_busy():
                pygame.mixer.Channel(6).stop()
            pygame.mixer.Channel(6).play(self.sound_select)
            select = True
        else:
            logger.error(f"Invalid keypress: {key}")
            if pygame.mixer.Channel(6).get_busy():
                pygame.mixer.Channel(6).stop()
            pygame.mixer.Channel(6).play(self.sound_next)

        if character == 0:
            current_text = "[locked]"
            self.rect.x = 0
            return;
        else:
            if character == 1:
                current_text = "Dark Ninja"
            elif character == 2:
                current_text = "Masked Ninja"
            elif character == 3:
                current_text = "Skeleton"
            elif character == 4:
                current_text = "Inspector"
        if character == 0:
            self.rect.x = 0
        else:
            self.rect.x = 76 * (character)
        if not select:
            return;
        elif select:
            ProfileIcon.store_character(current_text)
            SelectionScreen.running = False

selectBox = Box(0, 0)


class ProfileIcon(pygame.sprite.Sprite):
    selected = 0
    def __init__(self, image, x, y):
        super().__init__()
        self.image: pygame.surface.Surface = image
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    @staticmethod
    def store_character(character: str):
        """ Puts character name into meta.json for main file to read """
        data = dict()
        character = character
        try:
            logger.debug("Loading character (attempting io operation)")
            # NOTE 1. Load json data
            logger.debug("Reading ./meta.json")
            with open('src/data/meta.json', 'r') as fp:
                data = json.load(fp)
                fp.close()
            # NOTE 2. change character value (currently null)
            logger.debug("Dumping to ./meta.json")
            data["character"] = character
            # NOTE 3. put back in json file
            with open('src/data/meta.json', 'w') as fp:
                json.dump(data, fp)
                fp.close()
        finally:
            logger.info(f"Stored as {character}")


class SelectionScreen:
    running = True  # NOTE: Needs to be accessed by ProfileIcon

    def __init__(self):
        self.image_path = image_path

        self.spritesheet = utils.Spritesheet(self.image_path)
        self.profile_icons = []
        self.screen = pygame.display.get_surface()
        self.load_profiles()

        self.sound_init = pygame.mixer.Sound(os.path.join(sfx, "choose_character.wav"))
        self.selection_music = pygame.mixer.Sound("assets/Music/1 - Adventure Begin.ogg")
        pygame.display.set_caption("Ninja Adventure - Choose Your Character!")

        self.queue = []

        pygame.mixer.Channel(1).set_volume(.1)
        pygame.mixer.Channel(6).set_volume(.2)
        pygame.mixer.Channel(1).play(self.selection_music)


        self.preview = PreviewBox(self.screen.get_width() - 150, 25)
        self.textbox = TextBox(self.preview.rect.x, self.preview.rect.height + 5, 55)
        self.draw()
        self.screen.blit(selectBox.image, selectBox.rect)
        self.textbox.draw(current_text, 0)

        self.current_character: ProfileIcon | None = None

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
                        38, 40), (20, 27, 27)), x, 0)
            self.profile_icons.append(icon)
            x += 76

    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                pygame.Rect(
                    (self.screen.get_width() - (self.preview.rect.width * 2)) - 10,
                    10,
                    10,
                    self.screen.get_height()-10),
                5, 5)

        for icon in self.profile_icons:
            self.screen.blit(icon.image, icon.rect)


        self.preview.draw(self.screen)
        self.screen.blit(
                self.profile_icons[ProfileIcon.selected].image,
                (self.preview.rect.x + 10, self.preview.rect.y + 10))

    def update(self):
        if SelectionScreen.running:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if (ProfileIcon.selected) == len(self.profile_icons) - 1:
                            ProfileIcon.selected = 0
                        else:
                            ProfileIcon.selected += 1
                        selectBox.select(ProfileIcon.selected)
                    if event.key == pygame.K_LEFT:
                        if ProfileIcon.selected == 0:
                            ProfileIcon.selected = len(self.profile_icons) - 1
                        else:
                            ProfileIcon.selected -= 1

                    selectBox.select(ProfileIcon.selected, event.key)

            self.draw()
            self.screen.blit(selectBox.image, (selectBox.rect.x, selectBox.rect.y))
            self.textbox.draw(current_text, time.time())
        else:
            return

class PreviewBox(pygame.sprite.Sprite):
    """ Shows player avatar and stats """
    def __init__(self, x, y, group=None):
        if group:
            super().__init__(group)
        else:
            super().__init__()
        self.image = pygame.image.load('assets/HUD/Dialog/FacesetBox.png').convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale_by(self.image, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, self.rect)
