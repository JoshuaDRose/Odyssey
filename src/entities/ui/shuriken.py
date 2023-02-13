import pygame


class Shuriken(pygame.sprite.Sprite):
    """ Used as a UI element to indicate attack damage on main hud and character selection screen """
    count = 0
    y = 2
    def __init__(self, x, y, group):
        super().__init__(group)
        self.screen = pygame.display.get_surface()
        self.image = pygame.image.load('assets/HUD/Shuriken.png').convert_alpha()

        self.image = pygame.transform.scale_by(self.image, 2)
        self.image.set_colorkey((0, 0, 0))

        # NOTE set rect after image as image is scaled and rect is not.
        self.rect = self.image.get_rect()

        self.rect.x = Heart.x + 3 + x
        self.rect.y = y

        Shuriken.x += self.rect.width + 3


    def draw(self) -> None:
        """ Draws self.image to surface parameter in the self.rect position """
        self.screen.blit(self.image, self.rect)
