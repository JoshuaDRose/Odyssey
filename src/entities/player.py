import os
import sys

import utils
import entities

import pygame
from loguru import logger


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)

        try:
            with open('src/data/meta.json') as fp:
                data = json.load(fp)
                character = data['character']
                ftp = data['ftp']
                fp.close()
        except FileNotFoundError:
            # NOTE: this will likely never happen as path checks are done for json 
            # files before this even runs
            logger.critical("Could not find essential files: meta.json")
            # NOTE: code 1 is exit vode
            sys.exit(1)

        self.image = pygame.image.load('assets/Actor/Characters/Boy/').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        w, h = self.image.get_size()
        self.rect = pygame.Rect(x, y, w, h)
        self.velocity = pygame.math.Vector2(250, 250)
        self.position = pygame.math.Vector2(self.rect.x, self.rect.y)

    def handle_keys(self):
        """ Player keypresses are handled within this method """
        if self.velocity.magnitude() > 0:
            self.velocity.normalize()

        key = pygame.key.get_pressed()

        self.position.x += (key[K_s] - key[K_a]) * self.velocity.x * dt
        self.position.y += (key[K_r] - key[K_w]) * self.velocity.y * dt
        self.position.x = max(0, min(camera.background.size[0] - 20, self.position.x))
        self.position.y = max(0, min(camera.background.size[1] - 20, self.position.y))

    def draw(self):
        """ Draw self.image and self.rect to current display (window) """
        pos = [self.position.x, self.position.y]

        for i in range(2):
            if camera.center[i] < pos[i] <= camera.background.size[i] - camera.center[i]:
                pos[i] = camera.center[i]
            elif pos[i] > camera.background.size[i] - camera.center[i]:
                pos[i] = camera.size[i] - camera.background.size[i] + pos[i]

        window.blit(self.image, (int(pos[0]), int(pos[1])))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
