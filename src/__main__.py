import os
import sys
import pygame
import entities
import utilities as utils
from loguru import logger

logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")

class window:
    done = False
    width, height = utils.get_size(True, True)


player = entities.Player(
        x = 100,
        y = 100)

logger.debug("Current folder: {}", utils.get_folder( utils.get_parent(os.getcwd()), __file__), feature='f-strings')
screen = pygame.display.set_mode((window.width, window.height), 0, 32)
pygame.display.set_caption("Ninja Adventure")
