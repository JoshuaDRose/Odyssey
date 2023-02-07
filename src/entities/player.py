import json
import os
import sys

from utils import Spritesheet

import pygame
from loguru import logger

from pygame import K_w, K_s, K_a, K_r
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT

ACC = 0.20

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)

        character = str()

        try:
            with open('src/data/meta.json') as fp:
                data = json.load(fp)
                character = data['character']
        except FileNotFoundError:
            logger.critical("Could not find essential files: meta.json")
            sys.exit(1)

        self.x = x
        self.y = y

        self.lastkey = 'r'

        self.character = character.replace(' ', '', character.count(' '))
        self.path = f'assets/Actor/Characters/{self.character}/SeparateAnim/'
        self.character = self.character.lower()

        self.walk_down = self.load_walk_cycle("down")
        self.walk_up = self.load_walk_cycle("up")
        self.walk_left = self.load_walk_cycle("left")
        self.walk_right = self.load_walk_cycle("right")

        self.idle_down = self.load_idle_cicle("down")
        self.idle_up = self.load_idle_cicle("up")
        self.idle_left = self.load_idle_cicle("left")
        self.idle_right = self.load_idle_cicle("right")

        self.animation = self.idle_down
        if not isinstance(self.animation, list):
            self.animation = [self.animation]

        self.frame = 0
        self.tick = 0
        self.fps = 10

        self.image = self.animation[self.frame]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity = pygame.math.Vector2(0, 0)
        self.accel = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.friction = -0.25

    def load_idle_cicle(self, direction):
        """ Load character idle cycle (one animation per direction) """
        images = []

        # NOTE Manually assign colormask
        colorkey = (0, 0, 0)
        if self.character == 'darkninja':
            print("Setting to black")
            colorkey = (0, 0, 0)
        elif self.character == 'skeleton':
            # BUG/TODO: fix skeleton bounding box
            colorkey = (255, 255, 255)
        elif self.character == 'maskedninja':
            colorkey = (255, 255, 255)

        sprite_sheet = Spritesheet(os.path.join(self.path, 'Idle.png'))

        if direction == "down":
            image = sprite_sheet.image_at((0, 0, 16, 16), colorkey)
            images.append(image)
        elif direction == "up":
            image = sprite_sheet.image_at((16, 0, 16, 16), colorkey)
            images.append(image)
        elif direction == "left":
            image = sprite_sheet.image_at((32, 0, 16, 16), colorkey)
            images.append(image)
        elif direction == "right":
            image = sprite_sheet.image_at((48, 0, 16, 16), colorkey)
            images.append(image)

        return images



    def load_walk_cycle(self, direction):
        """ Loads character walk cycle (can be dynamic) """
        images = []

        # NOTE Manually assign colormask
        colorkey = (0, 0, 0)
        if self.character == 'darkninja':
            colorkey = (0, 0, 0)
        elif self.character == 'skeleton':
            # BUG/TODO: fix skeleton bounding box
            colorkey = (255, 255, 255)
        elif self.character == 'maskedninja':
            colorkey = (255, 255, 255)

        sprite_sheet = Spritesheet(os.path.join(self.path, 'Walk.png'))

        with open('src/data/player_data.json') as fp:
            data = json.load(fp)
            for image in data["walk"][direction].values():
                images.append(sprite_sheet.image_at((image[0], image[1], 16, 16), colorkey))
        return images

    def handle_keys(self):
        """ Player keypresses are handled within this method """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.accel.x = 0
        self.accel.y = 0

        keys = pygame.key.get_pressed()

        keydown = False
        # lastkey = 'r'

        if keys[K_LEFT] or keys[K_a]:
            keydown = True
            self.lastkey = 'a'
            self.accel.x = -ACC
            self.animation = self.walk_left
        if keys[K_RIGHT] or keys[K_s]:
            self.lastkey = 's'
            keydown = True
            self.accel.x = ACC
            self.animation = self.walk_right
        if keys[K_UP] or keys[K_w]:
            self.lastkey = 'w'
            self.accel.y = -ACC
            keydown = True
            self.animation = self.walk_up
        if keys[K_DOWN] or keys[K_r]:
            self.lastkey = 'r'
            keydown = True
            self.accel.y = ACC
            self.animation = self.walk_down

        if not keydown:
            print('idle')
            if self.lastkey == 'a':
                self.animation = self.idle_left
                self.frame = 0
            elif self.lastkey == 's':
                self.animation = self.idle_right
                self.frame = 0
            elif self.lastkey == 'w':
                self.animation = self.idle_up
                self.frame = 0
            elif self.lastkey == 'r':
                self.animation = self.idle_down
                self.frame = 0

        self.accel.x += self.velocity.x * self.friction
        self.accel.y += self.velocity.y * self.friction
        self.velocity += self.accel
        self.position += self.velocity + 0.5 * self.accel

    def update_collision(self):
        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)

    def update(self):
        if self.tick >= self.fps:
            if self.frame >= len(self.animation)-1:
                self.frame = 0
            else:
                self.frame += 1
            self.tick = 0

        self.image = self.animation[self.frame]
        self.tick += 1
        self.update_collision()
