'''
    
'''

from pymxs import runtime as mxs # pylint: disable=import-error
from qtmax import GetQMaxMainWindow # pylint: disable=import-error

#~ from ...vendor.Qt import QtWidgets, QtGui, QtCore 
#~ from ...lib import utils as utils, widgets, settings, preset, encode
#~ from .... import PLAYBLAST_PLUS_MODULE_ROOT as module_root
#~ from .max_scene import Max_Scene as scene
#~ from .max_logger import MaxLogger

from playblast_plus.vendor.Qt import QtWidgets, QtGui, QtCore 
from playblast_plus.lib import utils as utils, widgets, settings, preset, encode
from playblast_plus import PLAYBLAST_PLUS_MODULE_ROOT as module_root
from playblast_plus.hosts.max.max_scene import Max_Scene as scene
from playblast_plus.hosts.max.max_logger import MaxLogger

from pathlib import Path

UI_NAME = "maxpreview_plus_dialog"

class MaxPreviewLogger(MaxLogger):
    """
    Set up a custom script logger
    """
    LOGGER_NAME = "MaxPreviewLogger"

def create_cylinder():
    """
    Create a cylinder node with predetermined radius and height values.
    """
    mxs.Cylinder(radius=10, height=30)
    # force a viewport update for the node to appear
    mxs.redrawViews()

class MaxPlayblastPlus(QtWidgets.QDialog):
    """
    Custom dialog attached to the 3ds Max main window
    Message label and action push button to create a cylinder in the 3ds Max scene graph
    """
    def __init__(self, parent=None):
        super(MaxPlayblastPlus, self).__init__(parent)
        #~ self.setWindowTitle('Max Preview Plus')
        self.init_ui()
        
        self.setObjectName(UI_NAME)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle("")

    def init_ui(self):
        """ Prepare Qt UI layout for custom dialog """

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setMargin(2)
        main_layout.setSpacing(6)
        main_layout.setAlignment(QtCore.Qt.AlignTop)


        header = widgets.ToolHeader('pbp_header', 'Create Preview ')  
        main_layout.addWidget(header)
        
        preview_btn = QtWidgets.QPushButton("Create Preview")
        preview_btn.setStyleSheet(widgets.Styles.BUTTON_HERO)
        preview_btn.clicked.connect(create_cylinder)
        main_layout.addWidget(preview_btn)
        
        capture_button = QtWidgets.QPushButton("SNAP")
        capture_button.setStyleSheet(widgets.Style.BUTTON_SIDEKICK)


        self.setLayout(main_layout)
        self.resize(290, 100)
        
        self._TEMPLATES = {}
        self._CAMERAS = scene.get_scene_cameras()
        self._SETTINGS = settings.get_config()
        self._SETTINGS['ui']['output_token']
        self._TEMPLATES = preset.load_templates ( [str(module_root / 
                                          self._SETTINGS['studio_templates'] )] )
        self.current_playblast_directory = scene.get_output_dir()
        
        #~ self._create_actions()
        #~ self._create_widgets()
        #~ self._connect_signals()

def run(*args):
    """
    Entry point for QDialog demo making use of PySide2 and pymxs
    """
    # Worth checking FFMpeg is installed correctly on the local system
    ffmpeg_path = settings.get_ffmpeg_path()
    if Path(ffmpeg_path).exists():
        tool = MaxPlayblastPlus(GetQMaxMainWindow())
        tool.show()
        MaxPreviewLogger.info(f"MaxPreviewPlus {args[0].version} Running...")
    else:
        mxs.pushPrompt(
                f'FFMpeg is not installed in the directory specified : {ffmpeg_path}') 
        MaxPreviewLogger.warning(
                f'Install FFMPeg to this location or edit the following file to point at your install : {settings.filepath()}')

if __name__ == "__main__":
    from playblast_plus import version
    run(version)