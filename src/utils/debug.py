""" Used for debugging, as name suggests :) """
import utils
import pygame



class Textbox(pygame.sprite.Sprite):
    fontPath = pygame.font.match_font('InconsolataLGC Nerd Font')

    def __init__(self, x, y):
        pygame.font.init()
        


def text():
    """ Display text in a small debug window """
    raise NotImplementedError
