import sys
from pathlib import Path

class HostEnv():

    def __init__(self) -> None:
        self.name = self.get_name()
        self.executable = self.get_executable()

    @classmethod
    def get_name(cls) -> str:
        """_summary_
        Returns:
            str: _description_
        """
        host_exe = cls.get_executable()
        return ( str( host_exe.stem ).lower())
    @classmethod
    def get_executable(cls) -> Path:
        """_summary_
        Returns:
            Path: _description_
        """
        return Path(sys.executable)

class Host():
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
        """
        should I make setters and getters for this? 
        """
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