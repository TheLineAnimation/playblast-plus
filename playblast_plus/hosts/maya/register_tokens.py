from ...lib import tokens
from .maya_scene import Maya_Scene

# host/scene based tokens
def _camera_token():

    camera=Maya_Scene.get_current_camera()
    """Return short name of camera from capture options"""
    camera = camera.rsplit("|", 1)[-1]  # use short name
    camera = camera.replace(":", "_")   # namespace `:` to `_`
    return camera

tokens.register_token("<camera>", 
                lambda options: _camera_token(),
                label="Insert camera name")
               
tokens.register_token("<scene>", 
                lambda options: Maya_Scene.get_name() or "playblast",
                label="Insert current scene name")               
               
tokens.register_token("<output_dir>",
                lambda options: Maya_Scene.get_output_dir(),
                label="Insert current working directory")