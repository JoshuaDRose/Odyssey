import pygame
import os


class Choice(pygame.sprite.Sprite):
    """ Display choice with yes and no option on specified x and y positions """
    def __init__(self, x, y):
        super().__init__()
        # self.image = os.path.join('./assets/HUD/Dialog/YesButton.png')
        self.image = pygame.image.load('assets/HUD/Dialog/ChoiceBox.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Button(pygame.sprite.Sprite):
    """ Button, can be used in choice class as well """
    def __init__(self, x, y, image, group):
        """ Constructor inherits all sprite methods, draw is overriden unless
            called from an instance of pygame.sprite.Group().draw()
        """
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface) -> None:
        """ Draw image to surface at position of rect """
        surface.blit(self.image, self.rect)
