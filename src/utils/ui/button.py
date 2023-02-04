import pygame
import os
from loguru import logger


class Choice(pygame.sprite.Sprite):
    """ Display choice with yes and no option on specified x and y positions """
    def __init__(self, x, y):
        super().__init__()
        # self.image = os.path.join('./assets/HUD/Dialog/YesButton.png')
        self.image = pygame.image.load('assets/HUD/Dialog/ChoiceBox.png').convert_alpha()
        self.screen = pygame.display.get_surface()
        try:
            self.image = pygame.transform.scale_by(self.image, 4)
        except AttributeError:
            logger.critical("Please upgrade pygame. This feature *is* availabe, but exclusively in pygame 2.1.3.devx")
        self.rect = self.image.get_rect()
        if x == True:
            self.rect.x = self.screen.get_width() // 2 - self.rect.width // 2
        else:
            self.rect.x = x
        if y == True:
            self.rect.y = self.screen.get_height() // 2 - self.rect.height // 2
        else:
            self.rect.y = y

        self.buttons = {
                "yes": Button(0, 0, 'assets/HUD/Dialog/YesButton.png'),
                "no": Button(0, 0, 'assets/HUD/Dialog/NoButton.png')}

        # NOTE scale all sprites 

        for i in self.buttons:
            self.buttons[i].image = pygame.transform.scale2x(self.buttons[i].image)
        """
        for button in self.buttons:
            self.buttons[button]
        """

        # NOTE rect.y is constant on all values in self.buttons
        for i in self.buttons:
            self.buttons[i].rect.y = self.rect.height // 2 - self.buttons[i].rect.height // 2

        self.choice = 0
        if not pygame.mouse.get_visible():
            pygame.mouse.set_visible(True)

    """
    @staticmethod
    def scale3x(image: pygame.surface.Surface):
        rect = image.get_rect()
        rect.width *= 3
        rect.height *= 3
        return pygame.transform.scale(image)
    """

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        ...

    def button_collided(self, mp):
        """
        mp: mouse position
        Detects if mouse is over self.buttons
        """
        for button in self.buttons.values():
            if pygame.Rect.collidepoint(button.rect, mp):
                if button == self.buttons["yes"]:
                    self.choice == 1
                elif button == self.buttons["no"]:
                    self.choice == -1


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

        self.path = image
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface) -> None:
        """ Draw image to surface at position of rect """
        surface.blit(self.image, self.rect)
