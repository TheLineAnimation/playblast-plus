from pathlib import Path
import sys
from playblast_plus.vendor.Qt import QtWidgets, QtCore

# Import Shiboken with fallback
try:
    from shiboken6 import wrapInstance
except ImportError:
    try:
        from shiboken2 import wrapInstance
    except ImportError:
        raise ImportError("Neither shiboken6 nor shiboken2 could be imported. Please install one of them.")

import maya.cmds as cmds
# import maya.OpenMayaUI as omui
from maya import OpenMaya, OpenMayaUI
            
from ...lib import scene


class Maya_Scene(scene.Scene):
    """
    An encapsualtion of methods that can describe a Maya scene file.

    Inherits From:
        scene (scene.Scene): scene base class
    """
    def main_window():
        """
        Returns the Maya main window widget as a Python object
        """
        main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        if sys.version_info.major >= 3:
            return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
        else:
            return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
        
    def ui_base_class():
        return (QtWidgets.QDialog)

    def get_widget(**kwargs):
        """ Deletes an already created widget

        Args:
            name (str): the widget object name
        """
        name = kwargs['name']

        # finds workspace control if dockable widget
        if cmds.workspaceControl(name, exists=True):
            cmds.workspaceControl(name, edit=True, clp=False)
            cmds.deleteUI(name)

        # finds the widget
        widget = OpenMayaUI.MQtUtil.findWindow(name)
        return widget


    def get_name(full_path: bool = False) -> str:
        """_summary_

        Args:
            full_path (bool, optional): _description_. Defaults to False.

        Returns:
            str: _description_
        """
        p = cmds.file(query=True, sceneName=True)
        if p:
            path = Path(p)
            if full_path:
                return str(path)
            else:
                return str(path.stem)
        return None

    def get_scene_cameras():
        """
        Returns the scene cameras, surprisingly
        """

        # all cameras
        # cameras = cmds.ls(type="camera", l=True)

        # all non startup cameras
        cameras = [c for c in cmds.ls(cameras=True) 
                        if not cmds.camera(c, q=True, startupCamera=True)] 
        return cameras
    
    def getFrameRate():
        """
        Return an int of the current frame rate
        """

        currentUnit = cmds.currentUnit(query=True, time=True)
        if currentUnit == 'film':
            return 24
        if currentUnit == 'show':
            return 48
        if currentUnit == 'pal':
            return 25
        if currentUnit == 'ntsc':
            return 30
        if currentUnit == 'palf':
            return 50
        if currentUnit == 'ntscf':
            return 60
        if 'fps' in currentUnit:
            return int(currentUnit.replace('fps',''))

        return 1
    
    def getFrameRange():
        start = cmds.playbackOptions(q=True, min=True)
        end = cmds.playbackOptions(q=True, max=True)
        return (start,end)
    
    def current_frame() -> int:
        """
        Return an integer of the current frame rate

        Fix To-DO - what if it's 29.97? 

        Returns:
            int: The scene's current frame rate
        """

        return cmds.currentTime(query=1)

    
    def get_render_resolution(self,multiplier=1.0):
        w = cmds.getAttr("defaultResolution.width")
        h = cmds.getAttr("defaultResolution.height")
        if multiplier != 1.0:
            w = int (w * multiplier)
            h = int (h * multiplier)
        return (w,h)
    
    def warning_message(text):
        OpenMaya.MGlobal.displayWarning(text)

    def info_message(text):
        OpenMaya.MGlobal.displayInfo(text)

    def error_message(text):
        OpenMaya.MGlobal.displayError(text)

    def set_viewport_camera(cam):
        if cam:
            cmds.lookThru(cam)
  
    def get_current_camera():
        """
        Returns the currently active camera.

        Searched in the order of:
            1. Active Panel
            2. Selected Camera Shape
            3. Selected Camera Transform

        Returns:
            str: name of active camera transform

            This doesn't work very well!! 
            need a better way to get the current camera from view
        """
        # Get the active model panel
        model_panels = cmds.getPanel(type="modelPanel")
        
        for panel in model_panels:
            if cmds.modelEditor(panel, query=True, activeView=True):
                camera = cmds.modelEditor(panel, query=True, camera=True)
                # Get just the short name
                # clean_camera = cmds.ls(camera, shortNames=True)[0]
                # return clean_camera
                return camera

        return None  # Fallback if no active panel is found

    def get_user_directory() -> str:
        # perhaps this should be the host class, it's not scene related
        maya_root = cmds.internalVar(uad=True)
        maya_version = cmds.about(version=True)
        return str (Path (maya_root , maya_version ))

    @classmethod             
    def get_output_dir(cls, workspace:bool = False) -> str:
        """Returns the playblast directory so that a filename can be specified.

        Args:
            workspace (bool, optional): Decides if the playblast is local to the 
            Maya install or the workspace location. Defaults to False.

        Returns:
            string: A folder location string
        """

        if workspace:
            playblast_dir = Path (cmds.workspace( q=True, dir=True ), 'playblasts' )
        else:
            user_dir = cls.get_user_directory()
            playblast_dir = Path (  user_dir , 'playblasts' )

        # make the directories if they do not exist
        playblast_dir.mkdir(parents=True, exist_ok=True)
        return str(playblast_dir)

