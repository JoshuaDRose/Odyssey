import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self,
                 image: pygame.surface.Surface,
                 x: int,
                 y: int, *groups):
        super().__init__(*groups)
        
