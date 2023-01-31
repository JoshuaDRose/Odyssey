import os
import sys
import pygame
import entities
import utilities as utils
from loguru import logger
from pygame import K_ESCAPE, QUIT

logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")

class Window:
    done = False
    width, height = utils.get_size(get_width=True, get_width=True)
    fps = 60

logger.debug("Current folder: {}", utils.get_folder( utils.get_parent(os.getcwd()), __file__), feature='f-strings')
screen = pygame.display.set_mode((Window.width, Window.height), 0, 32)
pygame.display.set_caption("Ninja Adventure")

player = entities.Player(
        x = 100,
        y = 100)

clock = pygame.time.Clock()

dt = 0
while not Window.done:
    for event in pygame.event.get():
        if event.type == QUIT:
            Window.done = True

    pygame.display.flip()
    dt = clock.tick(Window.fps) / 1000

pygame.quit()
sys.exit()
