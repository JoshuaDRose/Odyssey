import json
import os
import sys

from utils import Spritesheet
from entities.ui import Heart

import pygame
from loguru import logger

from pygame import K_w, K_s, K_a, K_r
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE

ACC = 0.20

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        character = str()

        try:
            with open('src/data/meta.json') as fp:
                data = json.load(fp)
                character = data['character']
        except FileNotFoundError as message:
            logger.critical("Could not find essential files: meta.json")
            raise(FileNotFoundError, message)

        self.x = x
        self.y = y

        self.do_report = False

        self.lastkey = 'r'

        self.up = False
        self.down = False
        self.left = False
        self.right = False

        self.character = character.replace(' ', '', character.count(' '))
        self.path = f'assets/Actor/Characters/{self.character}/SeparateAnim/'
        self.character = self.character.lower()

        self.ss_walk = Spritesheet(os.path.join(self.path, 'Walk.png'))

        self.tutorial_attack_hint = False

        i = 1

        self.walk_down = [
                #  NOTE 'y' rect needs to be one pixel down
                self.ss_walk.image_at((0, 0, 16, 16)),
                self.ss_walk.image_at((0, 16, 16, 16)),
                self.ss_walk.image_at((0, 32, 16, 16)),
                self.ss_walk.image_at((0, 48, 16, 16)),
            ]
        self.walk_up = [
                self.ss_walk.image_at((16, 0, 16, 16)),
                self.ss_walk.image_at((16, 16, 16, 16)),
                self.ss_walk.image_at((16, 32, 16, 16)),
                self.ss_walk.image_at((16, 48, 16, 16)),
            ]
        self.walk_left = [
                self.ss_walk.image_at((32, 0, 16, 16)),
                self.ss_walk.image_at((32, 16, 16, 16)),
                self.ss_walk.image_at((32, 32, 16, 16)),
                self.ss_walk.image_at((32, 48, 16, 16)),
            ]
        self.walk_right = [
                self.ss_walk.image_at((48, 0, 16, 16)),
                self.ss_walk.image_at((48, 16, 16, 16)),
                self.ss_walk.image_at((48, 32, 16, 16)),
                self.ss_walk.image_at((48, 48, 16, 16)),
            ]

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
        self.fps = 15

        self.image = self.animation[self.frame]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.health = 3 # 3 hearts

        self.hearts = pygame.sprite.Group()

        for _ in range(self.health):
            Heart(Heart.x, Heart.y, self.hearts)

        self.reset_heart_menu() # NOTE see docstring for util

        self.velocity = pygame.math.Vector2(0, 0)
        self.accel = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.friction = -0.25

    def draw(self, surface) -> None:
        surface.draw(self.image, self.rect)

    def load_idle_cicle(self, direction):
        """ Load character idle cycle (one animation per direction) """
        images = []
        """
        colorkey = (0, 0, 0)
        if self.character == 'maskedninja':
            colorkey = (255, 255, 255)
        elif self.character == 'skeleton':
            # BUG/TODO: fix bounding box
            colorkey = (255, 255, 255)
        elif self.character == 'grayninja':
            colorkey = (255, 255, 255)
        elif self.character == 'noble':
            # BUG/TODO: fix bounding box
            colorkey = (255, 255, 255)
        """
        sprite_sheet = Spritesheet(os.path.join(self.path, 'Idle.png'))

        if direction == "down":
            image = sprite_sheet.image_at((0, 0, 16, 16))
            images.append(image)
        elif direction == "up":
            image = sprite_sheet.image_at((16, 0, 16, 16))
            images.append(image)
        elif direction == "left":
            image = sprite_sheet.image_at((32, 0, 16, 16))
            images.append(image)
        elif direction == "right":
            image = sprite_sheet.image_at((48, 0, 16, 16))
            images.append(image)

        return images
    
    def load_walk_cycle(self, direction):
        """ Loads character walk cycle (can be dynamic) """
        # NOTE pygame needs external scope method assignment
        images = []
        # NOTE Manually assign colormask
        colorkey = (0, 0, 0)
        if self.character == 'maskedninja':
            colorkey = (255, 255, 255)
        elif self.character == 'skeleton':
            # BUG/TODO: fix bounding box
            colorkey = (255, 255, 255)
        elif self.character == 'grayninja':
            colorkey = (255, 255, 255)
        elif self.character == 'noble':
            # BUG/TODO: fix bounding box
            colorkey = (255, 255, 255)

        sprite_sheet = Spritesheet(os.path.join(self.path, 'Walk.png'))

        with open('src/data/player_data.json') as fp:
            data = json.load(fp)
            for image in data["walk"][direction].values():
                images.append(sprite_sheet.image_at((image[0], image[1], 16, 16)))
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

        if keys[K_LEFT] or keys[K_a]:
            keydown = True
            self.lastkey = 'a'
            self.left = 1
            self.accel.x = -ACC
            self.animation = self.walk_left
        if keys[K_RIGHT] or keys[K_s]:
            self.lastkey = 's'
            keydown = True
            self.right = 1
            self.accel.x = ACC
            self.animation = self.walk_right
        if keys[K_UP] or keys[K_w]:
            self.lastkey = 'w'
            self.accel.y = -ACC
            self.up = 1
            keydown = True
            self.animation = self.walk_up
        if keys[K_DOWN] or keys[K_r]:
            self.lastkey = 'r'
            self.down = 1
            keydown = True
            self.accel.y = ACC
            self.animation = self.walk_down
        if keys[K_SPACE]:
            # TODO => ONLY ATTACK IF NOT NEXT TO INTERACTABLE OBJECT
            if self.attack_available:
                self.animation = self.attack
            self.tutorial_attack_hint = True

        if not keydown:
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

    @property
    def attack_available(self) -> bool:
        """ TODO => this function should contain logic to detect if 
                    the player is next to an object. Return if this is 
                    true or false.
        """
        return False

    @property
    def report(self) -> bool:
        """ set conditional to run send_report """
        return all([self.up,
                self.down,
                self.left,
                self.right])

    @report.setter
    def report(self):
        """ set report property """
        # print((self.up, self.down, self.left, self.right))
        pass

    @report.deleter
    def report(self):
        """ remove report property """
        del self.do_report

    def reset_heart_menu(self):
        """ resets heart position from previous menu """
        x = 4
        y = 2

        for heart in self.hearts:
            heart.rect.x = x
            heart.rect.y = y
            x += heart.rect.width + 2

