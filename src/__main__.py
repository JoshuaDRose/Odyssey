import os
import sys

os.system('clear')

class Version:
    version = sys.version.split(' ')[0]
    major = int(version.split('.')[0])
    minor = int(version.split('.')[1])
    patch = int(version.split('.')[2])

if Version.major < 3:
    logger.critical("You are using python {}. Please use >= python3.7.0".format(Version.version))
    sys.exit(1)
elif Version.minor < 6:
    logger.critical("<=python3.6 is not supported")
    sys.exit(1)

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
# BUG: Caption cannot be redeclared unless the display from THIS SCOPE is parsed into a seperate file.
pygame.display.set_caption("Ninja Adventure")

if not pygame.mixer.get_init():
    logger.debug("Initializing pygame.mixer")

logger.info("[Mixer]\n Bitrate: {}\nChannels: {}", pygame.mixer.get_init()[0], pygame.mixer.get_num_channels(), feature="f-strings")

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

do_cache = True
check_wasd = False
check_attack = False


def add_mvmnt_cache():
    global do_cache, check_wasd, check_attack
    """ Add json configuration for tutorial movement sprites """
    path = os.path.join('src/data/cache', 'mvmnt.json')
    logger.debug(f"Adding movement cache to {path}")

    data = {
            "check_wasd": check_wasd,
            "check_attack": check_attack
            }
    if check_wasd is True and check_attack is not True:
        tutorial.current_tutorial_image.image = tutorial.tutorial_sprites[tutorial.move_index]
    elif check_attack is True:
        tutorial.current_tutorial_image.image = tutorial.tutorial_sprites[tutorial.attack_index]

    with open(path, 'w', True, 'utf8') as fp:
        json.dump(data, fp, ensure_ascii=True, sort_keys=True)
    do_cache = False

# NOTE Retrieve character from  json file
try:
    with open('src/data/meta.json') as fp:
        data = json.load(fp)
        character = data['character']
        ftp = data['ftp']
        fp.close()
except FileNotFoundError:
    # NOTE: this will likely never happen as path checks are done for json files before this even runs
    logger.critical("Could not find essential files: meta.json")
    # NOTE: code 1 is exit vode
    sys.exit(1)

# TODO: remove when redundant or ready
logger.debug("Loading main menu as {}.", character, feature="f-strings")

global tutorial
tutorial = levels.Tutorial()
ftp_query = True

if ftp:
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    tutorial_query.choice = -1
                elif event.key == pygame.K_RETURN:
                    tutorial_query.choice = 1
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
        tutorial.running = True
        while tutorial.running:
            tutorial.draw_sprites()
            if do_cache:
                if tutorial.player.report:
                    check_wasd = True
                    add_mvmnt_cache()
                    tutorial.current_tutorial_image.image = tutorial.tutorial_sprites[tutorial.attack_index]
                    if all([
                            tutorial.player.tutorial_attack_hint,
                            tutorial.player.do_report
                            ]):
                        check_attack = True
                        add_mvmnt_cache()
                        do_cache = False
                        logger.success("Note to self: end tutorial here - fade out idea?")

    elif tutorial_query.choice == -1:
        # NOTE Don't do tutorial, create level instance etc ...
        # TODO Setup tutorial as mentioned above
        logger.critical("Main levels aren\'t setup yet :(")
        sys.exit(0)

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
