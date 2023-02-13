""" Character selection screen """
import os
import time
import sys
import pygame
import json
import utils
from .debug import TextBox
from pygame import K_RIGHT, K_LEFT, AUDIO_ALLOW_FREQUENCY_CHANGE, AUDIO_ALLOW_CHANNELS_CHANGE
from loguru import logger

from entities.ui import Heart, Shuriken as Attack

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
    """ Character preview boxes (with white border """
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.Surface((76, 80), pygame.SRCALPHA)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.sound_next = pygame.mixer.Sound(os.path.join(sfx, "Menu2.wav"))
        self.sound_prev = pygame.mixer.Sound(os.path.join(sfx, "Menu3.wav"))
        self.sound_select = pygame.mixer.Sound(os.path.join(sfx, "Menu9.wav"))

    def select(self, character, key=pygame.K_RIGHT) -> None:
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
                current_text = "Masked Ninja"
            elif character == 2:
                current_text = "Gray Ninja"
            elif character == 3:
                current_text = "Skeleton"
            elif character == 4:
                current_text = "Noble"
        if character == 0:
            self.rect.x = 0
        else:
            self.rect.x = 76 * (character)

        # NOTE character is character index && current text is actual name
        logger.debug('damage: {}\nhealth: {}',
                     locations[current_text]['damage'],
                     locations[current_text]['health'],
                     feature='f-strings')

        if not select:
            return;
        ProfileIcon.store_character(current_text)
        SelectionScreen.running = False

selectBox = Box(0, 0)


class ProfileIcon(pygame.sprite.Sprite):
    selected = 0
    def __init__(self, image, x, y) -> None:
        super().__init__()
        self.image: pygame.surface.Surface = image
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface) -> None:
        # surface.blit(self.image, self.rect) TODO: removed or reinstance
        pass

    @staticmethod
    def store_character(character: str) -> None:
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

    def __init__(self) -> None:
        self.image_path = image_path

        self.spritesheet = utils.Spritesheet(self.image_path)
        self.profile_icons = []
        self.screen = pygame.display.get_surface()

        self.sound_init = pygame.mixer.Sound(os.path.join(sfx, "choose_character.wav"))
        self.selection_music = pygame.mixer.Sound("assets/Music/1 - Adventure Begin.ogg")
        pygame.display.set_caption("Ninja Adventure - Choose Your Character!")

        self.queue = []

        pygame.mixer.Channel(1).set_volume(.1)
        pygame.mixer.Channel(6).set_volume(.2)
        pygame.mixer.Channel(1).play(self.selection_music)

        # NOTE >> MUST BE RUN IN THIS EXACT ORDER
        self.preview = PreviewBox()
        self.selection = Statistics(self.preview.rect.bottom + 10)
        self.load_profiles()

        # self.screen.get_width() - 150 == print(self.preview.rect.x)
        self.textbox = TextBox(
                self.preview.rect.x,
                self.preview.rect.top - 25,
                30)

        self.draw()
        self.screen.blit(selectBox.image, selectBox.rect)
        self.textbox.draw(current_text, center=self.preview.rect)

        self.current_character: ProfileIcon | None = None

    def load_profiles(self) -> None:
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
                        38, 40)), x, 0)

            Attack.count = locations[character]['damage']
            Heart.count = locations[character]['health']

            # clear sprite groups
            logger.debug("Clearing heart group")
            self.selection.heart_group.empty()
            logger.debug("Clearing attack group")
            self.selection.attack_group.empty()

            self.selection.set_heart_count()
            self.selection.set_attack_count()

            self.profile_icons.append(icon)
            x += 76


    def draw(self) -> None:
        self.screen.fill((0, 0, 0))

        # NOTE box *image* around current selected player
        self.preview.draw(self.screen)

        self.screen.blit(
                self.profile_icons[ProfileIcon.selected].image,
                (self.preview.rect.x + 10, self.preview.rect.y + 10))
        # NOTE-TO-SELF: if textbox is drawn after it overwrites previous stat sprites
        self.textbox.draw(current_text, self.preview.rect)
        self.selection.draw(self.screen)

        # print(len(self.selection.heart_group.sprites())) >> 13. needs fix.

        for heart in self.selection.heart_group:
            heart.draw()

        for shuriken in self.selection.attack_group:
            shuriken.draw()


    def update(self) -> None:
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


class Statistics(object):
    """ container filled with player statistics """
    def __init__(self, y: int) -> None:
        screen = pygame.display.get_surface()
        self.image = pygame.Surface((150, 250))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, (255, 255, 255), self.rect, 2, 5)
        self.rect.x = screen.get_width() // 2 - self.rect.width // 2
        self.rect.y = y

        self.heart_group = pygame.sprite.Group()
        self.attack_group = pygame.sprite.Group()

        self.sprite_x_offset = 375

    def set_heart_count(self) -> None:
        """ Sets the heart count when a new character is selected """
        logger.debug("setting heart count @ {}", Heart.count, feature="f-strings")
        Heart.x = 4
        for _ in range(Heart.count):
            Heart(self.sprite_x_offset, 390, self.heart_group)
            Heart.increment_x_axis()

    def set_attack_count(self) -> None:
        """ Sets the attack count when a new character is selected """
        logger.debug("setting attack count @ {}", Attack.count, feature="f-strings")
        Attack.x = 4
        for _ in range(Attack.count):
            Attack(self.sprite_x_offset, 425, self.attack_group)
            Attack.increment_x_axis()

    def draw(self, surface: pygame.surface.Surface) -> None:
        surface.blit(self.image, self.rect)


class PreviewBox(pygame.sprite.Sprite):
    """ Shows player avatar and stats """
    def __init__(self) -> None:
        super().__init__()
        screen = pygame.display.get_surface()
        self.image = pygame.image.load('assets/HUD/Dialog/FacesetBox.png').convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale_by(self.image, 2)
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_width() // 2 - self.rect.width // 2
        self.rect.y = screen.get_height() // 2 - self.rect.height // 2
        self.rect.y -= 50

    def draw(self, surface: pygame.surface.Surface) -> None:
        surface.blit(self.image, self.rect)
