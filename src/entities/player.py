import json
import os
import sys

try:
    from ..utils import Spritesheet
except ImportError:
    try:
        from utils import Spritesheet
    except ModuleNotFoundError:
        pass

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

        self.x =  x
        self.y =  y

        self.character = character.replace(' ', '', character.count(' '))
        path = f'assets/Actor/Characters/{self.character}/SeparateAnim/'
        self.idle = Player.load_sequence(os.path.join(path, 'Idle.png'), self.character.lower())
        self.attack = Player.load_sequence(os.path.join(path, 'Attack.png'), self.character.lower())
        self.dead = Player.load_sequence(os.path.join(path, 'Dead.png'), self.character.lower())
        self.item = Player.load_sequence(os.path.join(path, 'Item.png'), self.character.lower())
        self.jump = Player.load_sequence(os.path.join(path, 'Jump.png'), self.character.lower())
        self.special1 = Player.load_sequence(os.path.join(path, 'Special1.png'), self.character.lower())
        self.special2 = Player.load_sequence(os.path.join(path, 'Special2.png'), self.character.lower())

        self.walk_down = self.load_walk_cycle("down")

        # TODO character UI

        """
        self.walk_up = Player.load_sequence(os.path.join(path, 'Walk.png'))[1]
        self.walk_left = Player.load_sequence(os.path.join(path, 'Walk.png'))[2]
        self.walk_right = Player.load_sequence(os.path.join(path, 'Walk.png'))[3]
        """

        self.animation = self.idle
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

    def load_walk_cycle(self, direction):
        """ Loads character walk cycle (can be dynamic) """
        images = []

        # NOTE Manually assign colormask
        colorkey = (0, 0, 0)
        if character == 'darkninja':
            colorkey = (0, 0, 0)
        elif character == 'skeleton':
            # BUG/TODO: fix skeleton bounding box
            colorkey = (255, 255, 255)
        elif character == 'maskedninja':
            colorkey = (255, 255, 255)

        file = os.path.split(sprite_sheet)[1].removesuffix('.png').lower()
        logger.info(f"[player] Loading animation from path: {sprite_sheet}", feature="f-strings")

        sprite_sheet = Spritesheet(
                os.path.join(path, 'Idle.png'), self.character.lower())

        with open('src/data/player_data.json') as fp:
            data = json.load(fp)
            for image in data["walk"][direction]:
                images.append(image)
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

        if keys[K_LEFT] or keys[K_a]:
            self.accel.x = -ACC
            self.animation = self.walk_left
        if keys[K_RIGHT] or keys[K_s]:
            self.accel.x = ACC
            self.animation = self.walk_right
        if keys[K_UP] or keys[K_w]:
            self.accel.y = -ACC
            self.animation = self.walk_up
        if keys[K_DOWN] or keys[K_r]:
            self.accel.y = ACC
            self.animation = self.walk_down

        self.accel.x += self.velocity.x * self.friction
        self.accel.y += self.velocity.y * self.friction
        self.velocity += self.accel
        self.position += self.velocity + 0.5 * self.accel

    def update_collision(self):
        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)

    def update(self):
        if self.tick >= self.fps:
            print(self.frame)
            if self.frame >= len(self.animation)-1:
                self.frame = 0
            else:
                self.frame += 1
            self.tick = 0

        self.image = self.animation[self.frame]
        self.tick += 1
        self.update_collision()
