from ...lib import tokens
from .max_scene import Max_Scene 

from pymxs import runtime as mxs

# register default tokens

# host/scene based tokens
def _camera_token(
        
    camera=Max_Scene.get_current_camera()):
    """Return short name of camera from capture options"""
    camera = camera.rsplit("|", 1)[-1]  # use short name
    camera = camera.replace(":", "_"
    )   
    return camera

tokens.register_token("<camera>", 
                lambda options: _camera_token(),
                label="Insert camera name")
               
tokens.register_token("<scene>", 
                lambda options: Max_Scene.get_name() or "playblast",
                label="Insert current scene name")               

tokens.register_token("<user>",
                lambda options :tokens.get_user_name(),
                label="Insert current user's name")
               
tokens.register_token("<output_dir>",
                lambda options: Max_Scene.get_output_dir(),
                label="Insert current working directory")

