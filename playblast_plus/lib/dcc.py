"""
    A class that encapsulates the host environment. 
    This binds the specific classes and functions that will be called in the
    specific DCC so the tool can function in multiple environments. 

    It detects the executable from sys.executable and uses the name to yield the 
    DCC.

"""

import sys
from pathlib import Path

class HostEnv():
    """
        HostEnv should perhaps be underscored as we don't want to call it directly,
        as it's instantiated by the Host class.
    """

    def __init__(self) -> None:
        self.name = self.get_name()
        self.executable = self.get_executable()

    @classmethod
    def get_name(cls) -> str:
        """ gets the name of the host
        Returns:
            str: the host name, eg. Maya, 3dsmax. 
        """
        host_exe = cls.get_executable()
        return ( str( host_exe.stem ).lower())
    @classmethod
    def get_executable(cls) -> Path:
        """Gets the current running executable 
        Returns:
            Path: The exe file as a pathlib.Path
        """
        return Path(sys.executable)

class Host():
    """
        Class to hold the DDC Environment. Each host subclasses the scene, 
        tokens and preview classes to provide common methods applicable to 
        each host.
    """
    def __init__(self) -> None:
        self._HOST_ENV = HostEnv()

        self.scene = None
        self.main_window = None
        self.preview = None
        self.name = self._HOST_ENV.name
        self.tokens = None
        self.executable = self._HOST_ENV.executable
        self.show_overrides = True
        self.UITEXT_image_plane = "Image Plane"
        self.UITEXT_preview = "Playblast"
        self.UIBASECLASS = None

        if self._HOST_ENV:
            if self._HOST_ENV.name == 'maya':
                from ..hosts.maya import maya_preview
                from ..hosts.maya.maya_scene import Maya_Scene
                from ..hosts.maya.register_tokens import tokens
                self.scene = Maya_Scene
                self.main_window = Maya_Scene.main_window()
                self.preview = maya_preview.Playblast()
                self.tokens = tokens
                self.UIBASECLASS = Maya_Scene.ui_base_class()

            elif self._HOST_ENV.name == '3dsmax':
                from ..hosts.max import max_preview
                from ..hosts.max.max_scene import Max_Scene
                from ..hosts.max.register_tokens import tokens
                self.scene = Max_Scene
                self.main_window = Max_Scene.main_window()
                self.preview = max_preview.MakePreview()
                self.tokens = tokens
                self.UITEXT_image_plane = "Viewport Background"
                self.UITEXT_preview = "Preview"
                self.UIBASECLASS = Max_Scene.ui_base_class()