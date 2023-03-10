""" Contains useful functions particularly relating to ease of use """

import os
import sys
import json
from loguru import logger

try:
    window = os.path.join('src/data', 'window.json')
except FileNotFoundError as error:
    logger.error(error)
    sys.exit(1)
    

def get_size(get_width=True, get_height=True) -> tuple[bool]:
    """ Description: Returns the size of window
        get_width: Return width   (default=true)
        get_height: Return height (default=true)
    """
    with open(window, 'r') as fp:
        content = json.load(fp)

    width = content['width'] if get_width else None
    height = content['height'] if get_height else None

    return (width, height)

def get_parent(directory):
    return os.path.dirname(os.path.relpath(directory))

def get_folder(dir, file):
    """ Returns the current directory appended to file """
    return os.path.join(dir, file)

def get_insert_paths(cwd) -> dict:
    with open(os.path.join(cwd, 'src/data/meta.json'), 'r') as fp:
        return json.load(fp)
