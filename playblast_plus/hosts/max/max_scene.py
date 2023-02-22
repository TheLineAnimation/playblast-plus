from pathlib import Path
from ...lib import scene

from pymxs import runtime as mxs

class Max_Scene(scene.Scene):
    def get_name(full_path: bool = False) -> str:

        path = Path (mxs.maxFilePath, mxs.maxFileName)
        if path.exists():
            if full_path:
                return str(path)
            else:
                return str(path.stem)
        return None

    def get_scene_cameras():
        """Returns the scene cameras, surprisingly

        other possible list comp is 
        [cam for cam in mxs.cameras if mxs.superclassOf(cam) == mxs.camera]
        """
        return [cam for cam in mxs.cameras if mxs.isKindOf(cam, mxs.camera)]
    
    def get_selected_object():
        selection = [s for s in mxs.selection]
        if len(selection) == 1:
            return (selection[0])
        else:
            return selection

    def get_current_camera():
        """Returns the currently active camera.

        Returns:
            obj: the active camera
        """
        return (mxs.viewport.GetCamera())
    
    def set_viewport_camera(cam):
        if mxs.isKindOf(cam, mxs.camera):
            mxs.viewport.SetCamera(cam)
        else:
            mxs.pushPrompt('Please provide a valid camera.')

    def get_animation_range():
        return mxs.animationRange
 
    # maybe use args here for different hosts             
    def get_output_dir(workspace:bool = False) -> str:
        """Returns the playblast directory so that a filename can be specified.

        Args:
            workspace (bool, optional): Decides if the playblast is local to the 
            Maya install or the workspace location. Defaults to False.

        Returns:
            string: A folder location string
        """
        return mxs.getDir( mxs.Name("preview"))
        