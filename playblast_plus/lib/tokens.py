from typing import Set, Union, Optional, List, Dict, Any, Tuple, Callable

"""Token system

The capture gui application will format tokens in the filename.
The tokens can be registered using `register_token`

"""
import maya.cmds as cmds
import maya_scene_data as maya_scene

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
    
def get_work_dir():
    
    """
    open_pype_server_root = os.getenv("OPENPYPE_PROJECT_ROOT_WORK") 
    open_pype_project = os.getenv("AVALON_PROJECT")
                open_pype_task = os.getenv("AVALON_TASK")             
    open_pype_shot = os.getenv("AVALON_ASSET") 
    open_pype_project = os.getenv("AVALON_PROJECT")            
    open_pype_work_dir = os.getenv("AVALON_WORKDIR")
    """

    import os
    return os.getenv('AVALON_WORKDIR', "FALLBACK")
    
def get_playblast_dir():
    
    """
    open_pype_server_root = os.getenv("OPENPYPE_PROJECT_ROOT_WORK") 
    open_pype_project = os.getenv("AVALON_PROJECT")
                open_pype_task = os.getenv("AVALON_TASK")             
    open_pype_shot = os.getenv("AVALON_ASSET") 
    open_pype_project = os.getenv("AVALON_PROJECT")            
    open_pype_work_dir = os.getenv("AVALON_WORKDIR"
    MAYA_APP_DIR

    """

    from pathlib import Path
    playblast_dir = Path (os.getenv('AVALON_WORKDIR', 
                            cmds.workspace( q=True, dir=True ))) / 'playblasts'
    playblast_dir.mkdir(parents=True, exist_ok=True)
    return str(playblast_dir)

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
                lambda options: get_playblast_dir(),
                label="Insert current working directory")


if __name__ == '__main__':
    outPath = format_tokens('<playblast_dir>',_registered_tokens)
    # out_str = format_tokens('<playblast_dir>_<scene>_<camera>_Bumholes_<user>', _registered_tokens )
    print (outPath)  

    