import maya.cmds as cmds
import os

def get_name():
    path = cmds.file(query=True, sceneName=True)
    if path:
        return os.path.splitext(os.path.basename(path))[0]
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

def get_current_camera():
    """Returns the currently active camera.

    Searched in the order of:
        1. Active Panel
        2. Selected Camera Shape
        3. Selected Camera Transform

    Returns:
        str: name of active camera transform
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
                                    
def get_playblast_dir(workspace:bool = False) -> str:
    """Returns the playblast directory so that a filename can be specified.

    Args:
        workspace (bool, optional): Decides if the playblast is local to the 
        Maya install or the workspace location. Defaults to False.

    Returns:
        string: A folder location string
    """

    from pathlib import Path

    if workspace:
        playblast_dir = Path (cmds.workspace( q=True, dir=True )) / 'playblasts' 
    else:
        playblast_dir = Path (cmds.internalVar(uad=True)) / 'playblasts' 

    # make the directories if they do not exist
    playblast_dir.mkdir(parents=True, exist_ok=True)
    return str(playblast_dir)

