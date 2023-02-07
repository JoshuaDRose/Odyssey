import json
import os
import sys

import utils
import entities

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
        self.idle_down = Player.load_sequence(os.path.join(path, 'Idle.png'))[0]
        self.idle_up = Player.load_sequence(os.path.join(path, 'Idle.png'))[1]
        self.attack = Player.load_sequence(os.path.join(path, 'Attack.png'))
        self.dead = Player.load_sequence(os.path.join(path, 'Dead.png'))
        self.item = Player.load_sequence(os.path.join(path, 'Item.png'))
        self.jump = Player.load_sequence(os.path.join(path, 'Jump.png'))
        self.special1 = Player.load_sequence(os.path.join(path, 'Special1.png'))
        self.special2 = Player.load_sequence(os.path.join(path, 'Special2.png'))
        self.walk_down = Player.load_sequence(os.path.join(path, 'Walk.png'))[0]
        self.walk_up = Player.load_sequence(os.path.join(path, 'Walk.png'))[1]
        self.walk_left = Player.load_sequence(os.path.join(path, 'Walk.png'))[2]
        self.walk_right = Player.load_sequence(os.path.join(path, 'Walk.png'))[3]

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

    @staticmethod
    def load_sequence(path) -> list[pygame.surface.Surface]:
        """ Returns a list of positions relative to player_data.json file """
        images = []
        file = os.path.split(path)[1].removesuffix('.png').lower()
        logger.info(f"[player] Loading animation from path: {path}", feature="f-strings")
        spritesheet = utils.Spritesheet(path)
        with open('src/data/player_data.json') as fp:
            data = json.load(fp)
            for anim in data:
                if len(data[file]) > 0:
                    for item in data[file]:
                        if len(item) > 1:
                            for index, direction in enumerate(data[file][item]):
                                print(data[file][item])
                                img_list = spritesheet.load_strip((data[file][item][str(index)][0], data[file][item][str(index)][1], 16, 16), 4)
                                for image in img_list:
                                    image.set_colorkey((0, 0, 0))
                                    images.append(image)
                                return images

                        img_list = spritesheet.load_strip((data[file][item][0], data[file][item][0], 16, 16),
                                    len(data[file][item]))
                        for image in img_list:
                            image.set_colorkey((0, 0, 0))
                            images.append(image)
                        return images
                else:
                    for item in data[file]:
                        images.append(item)
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
        if keys[K_RIGHT] or keys[K_s]:
            self.accel.x = ACC

        self.accel.x += self.velocity.x * self.friction
        self.velocity += self.accel
        self.position += self.velocity + 0.5 * self.accel

    def draw(self):
        """ Draw self.image and self.rect to current display (window) """
        pass

    def update_collision(self):
        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)

    def update(self):
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        """
        if self.tick >= self.fps:
            if self.frame >= len(self.animation)-1:
                self.frame = 0
            else:
                self.frame += 1
            self.tick = 0

        self.image = self.animation[self.frame]
        self.tick += 1
