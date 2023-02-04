import pygame
import os
from loguru import logger


class Choice(pygame.sprite.Sprite):
    """ Display choice with yes and no option on specified x and y positions """
    def __init__(self, x, y):
        super().__init__()
        # self.image = os.path.join('./assets/HUD/Dialog/YesButton.png')
        self.image = pygame.image.load('assets/HUD/Dialog/ChoiceBox.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.buttons = {
                "yes": Button(0, 0, 'assets/HUD/Dialog/YesButton.png'),
                "no": Button(0, 0, 'assets/HUD/Dialog/NoButton.png')}
        self.choice = 0
        if not pygame.mouse.get_visible():
            pygame.mouse.set_visible(True)

    def draw(self, surface):
        for button in self.buttons.values():
            surface.blit(button.image, button.rect)

    def update(self):
        for button in self.buttons.values():
            # TODO: add code.
            if pygame.Rect.collidepoint(button.rect, mp):
                ...



class Button(pygame.sprite.Sprite):
    """ Button, can be used in choice class as well """
    def __init__(self, x, y, image: str, group=None):
        """ Constructor inherits all sprite methods, draw is overriden unless
            called from an instance of pygame.sprite.Group().draw()
        """
        if group:
            super().__init__(group)
        else:
            super().__init__()
        if not isinstance(image, str):
            logger.critical(f"Image loaded as {type(image)}, needs to be loaded as string")

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface) -> None:
        """ Draw image to surface at position of rect """
        surface.blit(self.image, self.rect)
