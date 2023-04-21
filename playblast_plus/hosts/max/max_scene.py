from pathlib import Path
from ...lib import scene
from ...vendor.Qt import QtWidgets

from pymxs import runtime as mxs 
import qtmax

"""
 def get_frame_range(self, **kwargs):

        current_in = int(pymxs.runtime.animationRange.start.frame)
        current_out = int(pymxs.runtime.animationRange.end.frame)
        return (current_in, current_out)

    def set_frame_range(self, in_frame=None, out_frame=None, **kwargs):

        pymxs.runtime.animationRange = pymxs.runtime.interval(in_frame, out_frame)

"""

class Max_Scene(scene.Scene):

    def main_window():
        """
        Return the Max main window widget as a Python object
        """
        main_window_qwdgt = qtmax.GetQMaxMainWindow()  
        return main_window_qwdgt
    
    # def get_widget(**kwargs):
    #     """ Deletes an already created widget

    #     Args:
    #         name (str): the widget object name
    #     """
    #     name = kwargs['name']
    #     # finds the widget
    #     # need to get a widget int from the name
    #     widget = QtWidgets.QWidget.find(name)
    #     return widget

    def ui_base_class():
        return ( QtWidgets.QDialog )

    def get_name(full_path: bool = False) -> str:

        path = Path (mxs.maxFilePath, mxs.maxFileName)
        if path.exists():
            if full_path:
                return str(path)
            else:
                return str(path.stem)
        return None
    
    def _is_empty_scene():
        return len(mxs.rootNode.Children) == 0


    def get_scene_cameras():
        """Returns the scene cameras, surprisingly

        other possible list comp is 
        [cam for cam in mxs.cameras if mxs.superclassOf(cam) == mxs.camera]
        """
        return [cam.name for cam in mxs.cameras if mxs.isKindOf(cam, mxs.camera)]
    
    def get_selected_object():
        selection = [s for s in mxs.selection]
        if len(selection) == 1:
            return (selection[0])
        else:
            return selection
        
    def current_frame():
        '''
        Return an int of the current frame rate
        q - what if it's 29.97? 
        '''
        return int(mxs.currentTime)

    def getFrameRate():
        '''
        Return an int of the current frame rate
        q - what if it's 29.97? 
        '''
        return int(mxs.frameRate)

    def getFrameRange() -> tuple:
        anim_range = mxs.animationRange
        return (int(anim_range.start),int(anim_range.end))
    
    def get_render_resolution(self,multiplier=1.0):
        return (mxs.renderWidth, mxs.renderHeight)

    def get_current_camera(**kwargs):
        """Returns the currently active camera.
        if name is passed from the function 

        Returns:
            obj: the active viewport camera or the named camera
        """
        cam_node =None
        if 'name' in kwargs:
            cam_node = (mxs.getNodeByName(kwargs['name']))
        # Just in case, we need to see if the name passed resolves into a camera
        # otherwise we return the active viewport
        if cam_node: 
            return cam_node
        else:
            return (mxs.viewport.GetCamera())
    
    def set_viewport_camera(cam):
        if mxs.isKindOf(cam, mxs.camera):
            mxs.viewport.SetCamera(cam)
        else:
            mxs.pushPrompt('Please provide a valid camera.')

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

    def get_user_directory() -> str:
        return mxs.getDir( mxs.Name("userScripts"))





        