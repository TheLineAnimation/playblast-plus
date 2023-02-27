from pathlib import Path
import sys
from playblast_plus.vendor.Qt import QtWidgets, QtCore
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
            
from ...lib import scene


class Maya_Scene(scene.Scene):
    """_summary_

    Args:
        scene (_type_): _description_
    """
    def main_window():
        """
        Return the Maya main window widget as a Python object
        """
        main_window_ptr = omui.MQtUtil.mainWindow()
        if sys.version_info.major >= 3:
            return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
        else:
            return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

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
        """Returns the scene cameras, surprisingly
        """

        # all cameras
        # cameras = cmds.ls(type="camera", l=True)

        # all non startup cameras
        cameras = [c for c in cmds.ls(cameras=True) 
                        if not cmds.camera(c, q=True, startupCamera=True)] 
        return cameras
    
    def getFrameRate():
        '''
        Return an int of the current frame rate
        '''
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
    
    def get_render_resolution(self,multiplier=1.0):
        w = cmds.getAttr("defaultResolution.width")
        h = cmds.getAttr("defaultResolution.height")
        if multiplier != 1.0:
            w = int (w * multiplier)
            h = int (h * multiplier)
        return (w,h)

    def get_current_camera():
        """Returns the currently active camera.

        Searched in the order of:
            1. Active Panel
            2. Selected Camera Shape
            3. Selected Camera Transform

        Returns:
            str: name of active camera transform

            This doesn't work very well!! 
            need a beeter way to get the current camera from view
        """
        
        # (check if the set has a camera defined)

        # Get camera from active modelPanel  (if any)
        panel = cmds.getPanel(withFocus=True)
        if cmds.getPanel(typeOf=panel) == "modelPanel":
            cam = cmds.modelEditor(panel, query=True, camera=True)
            # In some cases above returns the shape, but most often it returns 
            # the transform. Still we need to make sure we return the transform.
            if cam:
                if cmds.nodeType(cam) == "transform":
                    return cam
                # camera shape is a shape type
                elif cmds.objectType(cam, isAType="shape"):
                    parent = cmds.listRelatives(cam, parent=True, fullPath=True)
                    if parent:
                        return parent[0]

        # Check if a camShape is selected (if so use that)
        cam_shapes = cmds.ls(selection=True, type="camera")
        if cam_shapes:
            return cmds.listRelatives(cam_shapes,
                                    parent=True,
                                    fullPath=True)[0]

        # Check if a transform of a camShape is selected
        # (return cam transform if any)
        transforms = cmds.ls(selection=True, type="transform")
        if transforms:
            cam_shapes = cmds.listRelatives(transforms, 
                                            shapes=True, type="camera")
            if cam_shapes:
                return cmds.listRelatives(cam_shapes,
                                        parent=True,
                                        fullPath=True)[0] 

    def get_user_directory() -> str:
        # perhaps this should be the host class, it's not scene related
        maya_root = cmds.internalVar(uad=True)
        maya_version = cmds.about(version=True)
        return str (Path (maya_root , maya_version ))

    # maybe use args here for different hosts
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

