import json
import os
import sys

import utils
import entities

import pygame
from loguru import logger

from pygame import K_w, K_s, K_a, K_d
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT


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
        self.walk = Player.load_sequence(os.path.join(path, 'Walk.png'))

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

        self.velocity = pygame.math.Vector2(250, 250)
        self.position = pygame.math.Vector2(self.rect.x, self.rect.y)

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


    def handle_keys(self, dt):
        """ Player keypresses are handled within this method """

        key = pygame.key.get_pressed()

        self.position.x += (key[K_d] - key[K_a]) * self.velocity.x * dt
        self.position.y += (key[K_s] - key[K_w]) * self.velocity.y * dt
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.position.y += 1 * self.velocity.y + dt
                if event.key == pygame.K_w:
                    self.position.y -= 1 * self.velocity.y + dt
                if event.key == pygame.K_a:
                    self.position.x -= 1 * self.velocity.x + dt
                if event.key == pygame.K_d:
                    self.position.x -= 1 * self.velocity.x + dt
        pass
        """

    def draw(self):
        """ Draw self.image and self.rect to current display (window) """

        """
        if self.velocity.magnitude() > 0:
            self.velocity.normalize()

        pos = [self.position.x, self.position.y]

        for i in range(2):
            if camera.center[i] < pos[i] <= camera.background.size[i] - camera.center[i]:
                pos[i] = camera.center[i]
            elif pos[i] > camera.background.size[i] - camera.center[i]:
                pos[i] = camera.size[i] - camera.background.size[i] + pos[i]

        window.blit(self.image, (int(pos[0]), int(pos[1])))
        """

        pass

    def update_collision(self):
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, dt: float):
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        """
        self.handle_keys(dt)
        if self.tick >= self.fps:
            if self.frame >= len(self.animation)-1:
                self.frame = 0
            else:
                self.frame += 1
            self.tick = 0

        self.image = self.animation[self.frame]
        self.tick += 1

        self.update_collision()
