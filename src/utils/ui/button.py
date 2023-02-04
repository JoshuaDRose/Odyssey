import pygame
import os


class Choice(pygame.sprite.Sprite):
    """ Display choice with yes and no option on specified x and y positions """
    def __init__(self, x, y):
        super().__init__()
        # self.image = os.path.join('./assets/HUD/Dialog/YesButton.png')
        image = self.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Button(pygame.sprite.Sprite):
    """ Button, can be used in choice class as well """
    def __init__(self, x, y, group):
        super().__init__(group)
