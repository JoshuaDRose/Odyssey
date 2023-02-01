import pygame

class Background:
    """ Dataclass for the background, contains image size width etc """
    def __init__(self) -> None:
        self.image: pygame.surface.Surface = pygame.image.load('background0.png').convert()
        self.size: tuple[int] = self.image.get_size()
        self.width, self.height = self.image.get_size()

class Camera(pygame.sprite.Group):
    """ Contains the viewport for the user """
    def __init__(self):
        super().__init__(self)
        self.size = [500, 500]
        self.width, self.height = self.size
        self.background = Background()
        self.position = pygame.math.Vector2(0, 0)
        self.center = self.width // 2, self.height // 2

    def draw(self) -> None:
        """ Draw camera position relative to the center of the screen """
        self.position.x = max(0, min(self.background.width - self.width, player.position.x - 200))
        self.position.y = max(0, min(self.background.height - self.height, player.position.y - 200))
        window.blit(self.background.image, (-int(self.position.x), -int(self.position.y)))
        for sprite in sprites:
            window.blit(sprite.image, (-int(self.position.x - sprite.rect.x), -int(self.position.y - sprite.rect.y)))


