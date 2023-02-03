""" Character selection screen """
import os
import sys
import pygame
import json
import utils
from .debug import TextBox
from pygame import K_RIGHT, K_LEFT, AUDIO_ALLOW_FREQUENCY_CHANGE, AUDIO_ALLOW_CHANNELS_CHANGE
from pygame import K_UP, K_DOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from loguru import logger

if not pygame.mixer.get_init():
    pygame.mixer.init()

pygame.mixer.music.set_volume(1.0)

image_path = os.path.join('assets/Actor/Characters', 'AllPreview.png')
sfx = 'assets/sfx/Menu'
locations = json.load(open('src/profiles.json'))
current_text = "Choose your character"


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

    def select(self, character):
        global current_text
        if pygame.mixer.Channel(6).get_busy():
            pygame.mixer.Channel(6).stop()
        pygame.mixer.Channel(6).play(self.sound_next)

        if character == 0:
            current_text = "The One True Doge"
            self.rect.x = 0
            return;
        else:
            if character == 1:
                current_text = "Samurai Ninja"
            if character == 2:
                current_text = "Sand person"
            self.rect.x = 76 * (character)

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

class SelectionScreen:
    def __init__(self):
        self.image_path = image_path

        # NOTE covers have black bg
        self.spritesheet = utils.Spritesheet(self.image_path)
        self.profile_icons = []
        self.screen = pygame.display.get_surface()
        self.load_profiles()
        self.running = True

        self.sound_init = pygame.mixer.Sound(os.path.join(sfx, "choose_character.wav"))

        self.queue = []

        pygame.mixer.Channel(1).set_volume(.5)
        pygame.mixer.Channel(6).set_volume(.75)
        pygame.mixer.Channel(1).play(self.sound_init)
        
        self.textbox = TextBox(self.screen.get_width() // 2, self.screen.get_height() // 2, 55)

        self.draw()
        self.screen.blit(selectBox.image, selectBox.rect)
        self.textbox.draw(current_text)

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
        for icon in self.profile_icons:
            self.screen.blit(icon.image, icon.rect)
            
    def update(self):
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
                    selectBox.select(ProfileIcon.selected)
                self.draw()
                self.screen.blit(selectBox.image, selectBox.rect)
                self.textbox.draw(current_text)
                pygame.display.update()
