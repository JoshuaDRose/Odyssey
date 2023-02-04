import os
import sys
import pygame
import utils
import entities
from loguru import logger
from pygame import K_ESCAPE, QUIT


logger.remove()
logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time}</green> <level>{message}</level>")

pathDict = utils.get_insert_paths(os.getcwd())
pathList = []

for value in list(pathDict.values()):
    for item in value:
        pathList.append(item)

for path in pathList:
    logger.debug("Appending folder: {} to Workspace",
            path,
            feature='f-strings')
    sys.path.insert(0, path)

class Window:
    done = False
    width, height = utils.get_size(get_width=True, get_height=True)
    fps = 60

logger.debug("Workspace: {}",
             os.path.relpath(
                 utils.get_folder(
                     utils.get_parent(os.getcwd()), __file__)),
             feature='f-strings')

screen = pygame.display.set_mode((Window.width, Window.height), 0, 32)
selection_screen = utils.SelectionScreen()
pygame.display.set_caption("Ninja Adventure")

if not pygame.mixer.get_init():
    logger.debug("Initializing pygame.mixer")

logger.debug(f"""[Mixer]
Bitrate: {pygame.mixer.get_init()[0]}
Channels: {pygame.mixer.get_num_channels()}""", feature="f-strings""")

# TODO get player to work after selection screen is done
# player = entities.Player( x = 100, y = 100 )

clock = pygame.time.Clock()

selecting = True

if pygame.mouse.get_visible():
    pygame.mouse.set_visible(0)

# in loud voice (choose your character!)
while selection_screen.running:
    selection_screen.update()

    pygame.display.update()

while not Window.done:
    for event in pygame.event.get():
        if event.type == QUIT:
            Window.done = True

    pygame.display.flip()
    dt = clock.tick(Window.fps) / 1000

pygame.quit()
sys.exit()
