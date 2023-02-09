import pygame

class Shuriken(pygame.sprite.Sprite):
    """ Used as a UI element to indicate attack damage on main hud and character selection screen """
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = pygame.image.load('assets/HUD/Shuriken.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface) -> None:
        """ Draws self.image to surface parameter in the self.rect position """
        surface.blit(self.image, self.rect)
