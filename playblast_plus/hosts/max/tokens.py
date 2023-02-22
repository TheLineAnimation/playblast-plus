from typing import Set, Union, Optional, List, Dict, Any, Tuple, Callable

"""Token system

The capture gui application will format tokens in the filename.
The tokens can be registered using `register_token`

"""
from . import maya_scene

_registered_tokens = dict()

import os

def format_tokens(string, options):
    """Replace the tokens with the correlated strings

    Arguments:
        string (str): filename of the playblast with tokens.
        options (dict): The parsed capture options.

    Returns:
        str: The formatted filename with all tokens resolved

    """

    if not string:
        return string

    for token, value in _registered_tokens.items():
        if token in string:
            func = value['func']
            string = string.replace(token, func(options))

    return string

def register_token(token, func, label=""):
    assert token.startswith("<") and token.endswith(">")
    assert callable(func)
    _registered_tokens[token] = {"func": func, "label": label}

def list_tokens():
    return _registered_tokens.copy()

# this is an example function which retrieves the name of the current user
def get_user_name():
    import getpass
    return getpass.getuser()

# register default tokens
# scene based tokens
def _camera_token(camera=maya_scene.get_current_camera()):
    """Return short name of camera from capture options"""
    camera = camera.rsplit("|", 1)[-1]  # use short name
    camera = camera.replace(":", "_")   # namespace `:` to `_`
    return camera


register_token("<camera>", 
                lambda options: _camera_token(),
                label="Insert camera name")
               
register_token("<scene>", 
                lambda options: maya_scene.get_name() or "playblast",
                label="Insert current scene name")               

register_token("<user>",
                lambda options :get_user_name(),
                label="Insert current user's name")
               
register_token("<playblast_dir>",
                lambda options: maya_scene.get_playblast_dir(),
                label="Insert current working directory")


if __name__ == '__main__':
    outPath = format_tokens('<playblast_dir>',_registered_tokens)

    print (outPath)  

    