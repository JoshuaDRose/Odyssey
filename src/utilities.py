""" Contains useful functions particularly relating to ease of use """

import os
import sys
import json
from loguru import logger

try:
    window = os.path.join('src', 'window.json')
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
