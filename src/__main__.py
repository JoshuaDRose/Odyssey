import json
import os
import levels
import sys
import pygame
import utils
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

# NOTE: This screen is also declared in utils/selection.py/Selection class
screen = pygame.display.set_mode((Window.width, Window.height), 0, 32)
# BUG: pygame.get_display is called, and we need not assign selection_screen here.
selection_screen = utils.SelectionScreen()
# BUG: Caption cannot be redeclared unless the display from THIS SCOPE is parsed into a 
# seperate file.
pygame.display.set_caption("Ninja Adventure")

if not pygame.mixer.get_init():
    logger.debug("Initializing pygame.mixer")

logger.info(f"""[Mixer]
Bitrate: {pygame.mixer.get_init()[0]}
Channels: {pygame.mixer.get_num_channels()}""", feature="f-strings""")

clock = pygame.time.Clock()


if pygame.mouse.get_visible():
    # NOTE Default = 0
    pygame.mouse.set_visible(0)

while selection_screen.running:
    selection_screen.update()
    pygame.display.update()

# Character will later be set to a string, read from meta.json
character = None
ftp = None # NOTE ftp shortened ver. of first time playing

# NOTE Retrieve character from  json file
try:
    with open('src/data/meta.json') as fp:
        data = json.load(fp)
        character = data['character']
        ftp = data['ftp']
        fp.close()
except FileNotFoundError:
    # NOTE: this will likely never happen as path checks are done for json 
    # files before this even runs
    logger.critical("Could not find essential files: meta.json")
    # NOTE: code 1 is exit vode
    sys.exit(1)

# TODO: remove when redundant or ready
logger.debug(f"Loading main menu as {character}.")

tutorial = levels.Tutorial()
ftp_query = True

if ftp:

    # NOTE: IF FIRST TIME PLAYING GIVE OPTION TO DO TUTORIAL
    # TEXT: HEY THERE! I NOTICED THIS IS YOUR FIRST TIME PLAYING! WOULD YOU LIKE TO DO THE TUTORIAL?
    # OPTIONS: YES | NO

    tutorial_query = utils.Choice(True, True)
    while tutorial_query.choice == 0:
        screen.fill((242, 234, 241))
        for element in tutorial.text:
            screen.blit(tutorial.text[element]["render"],
                        tutorial.text[element]["rect"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                tutorial_query.button_collided(mp)
            elif event.type == pygame.MOUSEMOTION:
                mp = pygame.mouse.get_pos()
        tutorial_query.draw(screen)
        tutorial_query.update()

        pygame.display.flip()
        clock.tick(Window.fps)

    mp = tuple()
    if tutorial_query.choice == 1:
        while tutorial.running:
            tutorial.draw()
    elif tutorial_query.choice == -1:
        # NOTE Don't do tutorial, create level instance etc ...
        # TODO Setup tutorial as mentioned above
        pass


while not Window.done:
    for event in pygame.event.get():
        if event.type == QUIT:
            Window.done = True
    # NOTE filling display with black also prevents frame ghosting
    screen.fill((0, 0, 0))

    # ALTERNATIVE: pygame.display.update()
    pygame.display.flip()
    # NOTE not used currently but likely in the future for
    # frame time regulation.
    dt = clock.tick(Window.fps) / 1000

pygame.quit()
sys.exit()
