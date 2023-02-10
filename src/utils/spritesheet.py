"""
Taken from https://www.pygame.org/wiki/Spritesheet
!! I DO NOT OWN THIS CODE !!
"""
import pygame
from loguru import logger

class Spritesheet(object):
    def __init__(self, filename, alpha=True, colorkey=(0,0,0)):
        try:
            if alpha:
                self.sheet = pygame.image.load(filename).convert_alpha()
            else:
                self.sheet = pygame.image.load(filename).convert()
            self.sheet.set_colorkey(colorkey)
        except pygame.error as message:
            logger.critical('Unable to load spritesheet image: %s', filename)
            raise(SystemExit, message)

    def image_at(self, rectangle, colorkey=(0,0,0)):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey(colorkey)
        return image

    def images_at(self, rects):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect) for rect in rects]

    def load_strip(self, rect: tuple, image_count: int):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups)
