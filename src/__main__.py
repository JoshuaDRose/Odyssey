import json
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
        format="<white>{time}</white> <level>{message}</level>")

pathDict = utils.get_insert_paths(os.getcwd()).get('paths')
pathList = []

logger.debug(pathDict)

for item in list(pathDict):
    pathList.append(item)

for path in pathList:
    logger.info("Appending folder: {} to Workspace",
            path,
            feature='f-strings')
    sys.path.insert(0, path)

class Window:
    done = False
    width, height = utils.get_size(get_width=True, get_height=True)
    fps = 60

logger.info("Workspace: {}",
             os.path.relpath(
                 utils.get_folder(
                     utils.get_parent(os.getcwd()), __file__)),
             feature='f-strings')

screen = pygame.display.set_mode((Window.width, Window.height), 0, 32)
selection_screen = utils.SelectionScreen()
pygame.display.set_caption("Ninja Adventure")

if not pygame.mixer.get_init():
    logger.debug("Initializing pygame.mixer")

logger.info(f"""[Mixer]
Bitrate: {pygame.mixer.get_init()[0]}
Channels: {pygame.mixer.get_num_channels()}""", feature="f-strings""")

clock = pygame.time.Clock()

if pygame.mouse.get_visible():
    pygame.mouse.set_visible(0)

while selection_screen.running:
    selection_screen.update()
    pygame.display.update()

character = None

# NOTE Retrieve character from  json file
with open('meta.json') as fp:
    character = json.load(fp)['character']
    fp.close()

logger.debug(f"Loading main menu as {character}.")

# NOTE: IF FIRST TIME PLAYING GIVE OPTION TO DO TUTORIAL
# TEXT: HEY THERE! I NOTICED THIS IS YOUR FIRST TIME PLAYING! WOULD YOU LIKE TO DO THE TUTORIAL?
# OPTIONS: YES | NO


while not Window.done:
    for event in pygame.event.get():
        if event.type == QUIT:
            Window.done = True
    screen.fill((0, 0, 0))

    pygame.display.flip()
    dt = clock.tick(Window.fps) / 1000

pygame.quit()
sys.exit()
