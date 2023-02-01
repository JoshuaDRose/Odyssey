import os
import sys
import pygame

sys.path.insert(0, '~/projects/Ninja Adventure/src/utils/')

class Player(object):
    def __init__(self, x: int, y: int):
        """ [TODO!] Supported with animation and physics
            x: Horizontal position (px)
            y: Vertical position   (px)
        """
