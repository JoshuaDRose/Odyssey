import pygame
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
        for index, i in enumerate(self.buttons):
            if index == 0:
                self.buttons[i].rect.x = self.rect.width - 80
            else:
                self.buttons[i].rect.x = 30
            self.buttons[i].rect.y = self.rect.height // 2 - (self.buttons[i].rect.height // 2)
            self.image.blit(self.buttons[i].image, self.buttons[i].rect)

        self.choice = 0

        if not pygame.mouse.get_visible():
            pygame.mouse.set_visible(True)

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

            # BUG only tests for collision with rect that is relative 
            # to the bounding box. needs to add bounding box rect.
            if pygame.Rect.collidepoint(pygame.Rect(
                button.rect.x + self.rect.x,
                button.rect.y + self.rect.y,
                button.rect.width,
                button.rect.height), mp):

                if button.text.lower().endswith('yesbutton.png'):
                    self.choice = 1
                elif button.text.lower().endswith('nobutton.png'):
                    self.choice = -1
