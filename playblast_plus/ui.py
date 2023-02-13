
"""
Playblast Plus

huge thanks to Jerome Drese for his UI code from SmearDeform www.nodilus.com

"""

# imports
import os
from maya import cmds
from maya import OpenMaya, OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
from PySide2 import QtCore


# import playblast_plus

from pathlib import Path

from playblast_plus.lib import utils as utils
from playblast_plus.lib import widgets as widgets  
from playblast_plus.lib import settings as settings
from playblast_plus.lib import preset as preset
from playblast_plus.lib import encode as encode
from playblast_plus.lib import content_management

from playblast_plus.hosts.maya import capture as capture
from playblast_plus.hosts.maya import tokens as tokens
from playblast_plus.hosts.maya import maya_scene as maya_scene
from playblast_plus.hosts.maya.logger import MayaLogger

from playblast_plus import PLAYBLAST_PLUS_MODULE_ROOT as module_root

from typing import Union
import copy

# Globals
UI_NAME = "playblast_plus_dialog"

class PlayBlastPlusLogger(MayaLogger):
    """
    Set up a custom script logger
    """
    LOGGER_NAME = "PlayBlastPlusLogger"


class PlayblastPlusUI(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    """
    PlayBlastPlus User Interface
    """
    
    # CLASS LEVEL GLOBALS
    ICON_SIZE = QtCore.QSize (28, 28)
    LIST_ICONS = {
        "anim": QtGui.QIcon(":bezierCurve.svg"),
        "camera":QtGui.QIcon(":camera.svg"),
        "light":QtGui.QIcon(":pointLight.open.svg"),
        "model": QtGui.QIcon(":polyIcosahedron.svg"),
        "pipeline": QtGui.QIcon(":meshVarGroup.svg"),
        "render": QtGui.QIcon(":anisotropic.svg")
        }
    WF_OVERRIDE_LAYER_NAME = 'pbp_Wireframe_Override'
    
    def __init__(self, name, parent=None):
        super(PlayblastPlusUI, self).__init__(parent=parent)

        # checks for previous ui instances
        kill_ui("{}WorkspaceControl".format(UI_NAME))
        kill_ui(UI_NAME)

        # sets title and object name
        self.setWindowTitle("")
        self.setObjectName(UI_NAME)
        
        self.setMinimumWidth(250)
        
        self._TEMPLATES = {}
        self._SETTINGS = settings.get_config()
        self._CAMERAS = maya_scene.get_scene_cameras()
        self._OP_ENABLED = False

        # creates main layout widget
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setMargin(2)
        self.main_layout.setSpacing(6)
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)

        self._create_actions()

        # call the widget creation method
        self._create_widgets()
        # connects signals
        self._connect_signals()
        

        # populate the UI with data
        self.camera_list.clear()
        self.camera_list.addItems([c.replace('Shape','') for c in self._CAMERAS])
        self.tokens_field.setText(self._SETTINGS['default_token'])
        self.template_paths = preset.get_project_locations (str(module_root /self._SETTINGS['studio_templates'] ))
        self._TEMPLATES = preset.load_templates ( self.template_paths )
        self.current_playblast_directory = maya_scene.get_playblast_dir()
        
        # to identify the different presets, they are stored within a dictionary, 
        # so the first key is the name identifier
        template_names = [list(k.keys())[0] for k in self._TEMPLATES]
        PlayBlastPlusLogger.info(template_names)
        self.template_list.addItems( template_names)
        
        self.toggle_ui_state()
        

    def _connect_signals(self):
        """ Connects widget signals to functionalities
        """
        self.playblast_button.clicked.connect(self.create_playblast)
        self.capture_button.clicked.connect(self.capture_viewport)
        
        self.open_playblast_dir.triggered.connect(self.open_playblast_directory)
        self.purge_playblast_dir.triggered.connect(self.clear_playblast_directory)
        
        self.template_override_setting.toggled.connect(self.toggle_ui_state) 


        
    def _create_actions(self):

        self.copy_to_clipboard_setting = QtWidgets.QAction("Copy To Clipboard", self)
        self.copy_to_clipboard_setting.setCheckable(True)
        self.copy_to_clipboard_setting.setChecked(True)
        
        self.keep_images_setting = QtWidgets.QAction("Keep Intermediate Images", self)
        self.keep_images_setting.setCheckable(True)
        self.keep_images_setting.setChecked(False)
        
        self.template_override_setting = QtWidgets.QAction("Enable", self)
        self.template_override_setting.setCheckable(True)
        self.template_override_setting.setChecked(False)

        self.open_playblast_dir = QtWidgets.QAction("Open Playblast Directory", self)
        self.purge_playblast_dir = QtWidgets.QAction("Purge Contents", self)
        
        
        # self.open_playblast_dir.setIcon (icon)
        # def setIconText ()
        self.open_playblast_dir.setIconVisibleInMenu(True)

        # add the actions from create widgets to organise things better

    def _create_widgets(self):
        """ Creates the widget elements the user will interact with
        """

        self.menu_bar = QtWidgets.QMenuBar()       
        self.display_menu = self.menu_bar.addMenu("Settings")   
        self.display_menu.addAction(self.open_playblast_dir)

        # self.display_menu.addSeparator()
        folder_separator = QtWidgets.QLabel("<b>Template Overrides</b>")
        folder_separator_action = QtWidgets.QWidgetAction(self)
        folder_separator_action.setDefaultWidget(folder_separator)
        self.display_menu.addAction(folder_separator_action)
        self.display_menu.addAction(self.template_override_setting) 
        # self.display_menu.addSeparator()

        folder_separator = QtWidgets.QLabel("<b>Data Options</b>")
        folder_separator_action = QtWidgets.QWidgetAction(self)
        folder_separator_action.setDefaultWidget(folder_separator)

        self.display_menu.addAction(folder_separator_action)

        self.display_menu.addAction(self.copy_to_clipboard_setting)
        self.display_menu.addAction(self.keep_images_setting)
        self.display_menu.addAction(self.purge_playblast_dir)

        # creates full frame border around the entire UI
        # self.main_layout is the container for the enitre UI
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(7)
        frame_layout = QtWidgets.QVBoxLayout(frame)
        frame_layout.setMargin(2)
        frame_layout.setSpacing(2)

        main_layout = QtWidgets.QGridLayout(frame)
        
        main_layout.setMargin(2)
        main_layout.setSpacing(2)

        # bold font for the heading labels
        custom_font = QtGui.QFont()
        custom_font.setBold(True)

        # Add widgets to the layout
        # ToolHeader is a custom label widget imported from lib.widgets
        header = widgets.ToolHeader('pbp_header', 'Playblast Plus ')  
 
        cam_formlayout = QtWidgets.QGridLayout() 
        self.template_list = QtWidgets.QComboBox()
        cam_formlayout.addWidget(self.template_list)        
        self.camera_list = QtWidgets.QComboBox()

        
        # IF UI ICONS ARE NEEDED - cast Maya icons to qpixmap
        # # x resolution
        # pixmap = QtGui.QPixmap("{}/x_res.png".format(self.resource_path))
        # x_res = QtWidgets.QLabel()
        # x_res.setPixmap(pixmap)
        # x_res.setMaximumWidth(32)
  
        # # y resolution
        # pixmap = QtGui.QPixmap("{}/y_res.png".format(self.resource_path))
        # y_res = QtWidgets.QLabel()
        # y_res.setPixmap(pixmap)
        # y_res.setMaximumWidth(32)

        # # z resolution
        # pixmap = QtGui.QPixmap("{}/z_res.png".format(self.resource_path))
        # self.z_res = QtWidgets.QLabel()
        # self.z_res.setPixmap(pixmap)
        # self.z_res.setMaximumWidth(32)

        
        self.tokens_field = QtWidgets.QLineEdit()
        
        style = ("QLineEdit{"
                 "font: bold 10px;"
                 "color: rgb(0, 250, 50);"
                 "height: 12px;"
                 )

        self.tokens_field.setStyleSheet(style)

        # create
        style = ("QPushButton{"
                 "font: bold 12px;"
                 "color: rgb(220, 250, 250);"
                 "height: 40px;"
                 "background-color: rgb(85, 160, 20);"
                 "border:1px solid black;"
                 "border-radius:4px;}"
                 "QPushButton:pressed{"
                 "background-color: rgb(200, 120, 40);"
                 "}"
                 )
        self.playblast_button = QtWidgets.QPushButton("PLAYBLAST")
        self.playblast_button.setStyleSheet(style)

        # edit frame border and layout
        edit_frame = QtWidgets.QFrame()
        edit_frame.setFrameStyle(6)
        locations_layout = QtWidgets.QGridLayout(edit_frame)
        locations_layout.setMargin(4)
        locations_layout.setSpacing(4)

        # reset
        style = ("QPushButton{"
                 "font: bold 12px;"
                 "color: rgb(220, 250, 250);"
                 "height: 40px;"
                 "background-color: rgb(200, 120, 40);"
                 "border:1px solid black;"
                 "border-radius:4px;}"
                 "}"
                 "QPushButton:pressed{"
                 "background-color: rgb(200, 120, 40);"
                 )
        self.capture_button = QtWidgets.QPushButton("SNAP")
        self.capture_button.setStyleSheet(style)


        
        # Overides 
 
        overrides_frame = QtWidgets.QFrame()
        overrides_frame.setFrameStyle(6)
        
        overrides_layout = QtWidgets.QGridLayout(overrides_frame)
        overrides_layout.setColumnStretch(1,4)
        
        overrides_label = QtWidgets.QPushButton("Template Overrides")
        overrides_label.setCheckable(True)  
        overrides_label.setFont(custom_font)

        style = ("QPushButton{"
         "font: 10px;"
         "color: rgb(220, 250, 250);"
         "height: 25px;"
         # "background-color: rgb(250, 60, 80);"
         # "border:1px solid black;"
         # "border-radius:4px;}"
         "}"
         "QPushButton::checked{background:rgb(255, 0, 0);"
         )
        overrides_label.setStyleSheet(style)
        
        self.wireframe_box = QtWidgets.QCheckBox("Show Wireframe")
        self.wireframe_box.setChecked(False)
        
        self.show_imgplane_box = QtWidgets.QCheckBox("Show Image Plane")
        self.show_imgplane_box.setChecked(True)
        
        self.half_res_box = QtWidgets.QCheckBox("Half Res")
        self.half_res_box.setChecked(True)

        overrides_layout.addWidget(self.show_imgplane_box, 1,1,1,5,QtCore.Qt.AlignLeft)
        overrides_layout.addWidget(self.half_res_box,2,1,1,5,QtCore.Qt.AlignLeft)
        overrides_layout.addWidget(self.wireframe_box,3,1,1,5,QtCore.Qt.AlignLeft)

        # addWidget(widget, fromRow, fromColumn, rowSpan, columnSpan, alignment) 
        locations_label = QtWidgets.QLabel("Output Name")
        locations_label.setFont(custom_font)
        
        locations_layout.addWidget(locations_label,0,0,1,1)
        locations_layout.addWidget(self.tokens_field,1,0,1,4)    
        
        capture_frame = QtWidgets.QFrame()
        capture_frame.setFrameStyle(6)
        
        capture_layout = QtWidgets.QGridLayout(capture_frame)
        capture_layout.setMargin(4)
        capture_layout.setSpacing(4)
        # addWidget(widget, fromRow, fromColumn, rowSpan, columnSpan, alignment) 
        capture_layout.addWidget(self.playblast_button,1,0,1,3)
        capture_layout.addWidget(self.capture_button,1,3,1,1)
        capture_layout.addWidget(self.camera_list,0,0,1,4)
        
        # add widgets to layouts
        self.main_layout.addWidget(header)
        self.main_layout.setMenuBar(self.menu_bar)      
        
        self.main_layout.addWidget(frame)
        frame_layout.addLayout(cam_formlayout)
        frame_layout.addWidget(overrides_frame)    
        frame_layout.addWidget(edit_frame)
        frame_layout.addWidget(capture_frame)

    def get_render_resolution(self,multiplier=1.0):
        w = maya.cmds.getAttr("defaultResolution.width")
        h = maya.cmds.getAttr("defaultResolution.height")
        if multiplier != 1.0:
            w = int (w * multiplier)
            h = int (h * multiplier)
            PlayBlastPlusLogger.info(f'New Playblast Size {w}x{h}')
        return (w,h)

    def set_display_layer(self):
        geo = cmds.listRelatives(cmds.ls(geometry=True), p=True, path=True)
        wfGroup = cmds.createDisplayLayer(geo, n = self.WF_OVERRIDE_LAYER_NAME)
        
        wf_col = self._SETTINGS['wireframe_override_color']
        PlayBlastPlusLogger.info(f'wf_col {wf_col}')

        cmds.setAttr("{}.color".format(wfGroup), True)
        cmds.setAttr("{}.overrideRGBColors".format(wfGroup), True)
        cmds.setAttr("{}.overrideColorRGB".format(wfGroup), wf_col[0], wf_col[1], wf_col[2])
        
    def remove_display_layer(self):
        if self.wireframe_box.isChecked():
            try:
                cmds.delete(self.WF_OVERRIDE_LAYER_NAME)
            except:
                OpenMaya.MGlobal.displayWarning(f'Something went wrong deleting the display layer - {WF_OVERRIDE_LAYER_NAME}') 

    def set_overrides(self,template) -> dict:
        """
        Add all pbjects to display layer and set to black, then remove afterwards
        """
        
        viewport = cmds.getPanel( withFocus=True)
        if self.template_override_setting.isChecked(): 
            # is wireframe override on? 
            wf_override_state = self.wireframe_box.isChecked()
            template["viewport_options"]["wireframeOnShaded"] = wf_override_state
            
            if wf_override_state:
                self.set_display_layer()
            
            if 'modelPanel' in viewport:
                cmds.modelEditor(viewport, edit=True, wireframeOnShaded=wf_override_state)

            template["viewport_options"]["imagePlane"] = self.show_imgplane_box.isChecked()

            if self.half_res_box.isChecked():
            #    calculate the current res and halve it
                width, height = self.get_render_resolution(0.5)
                template["width"] = width
                template["height"] = height

        else:
            if 'modelPanel' in viewport:
                cmds.modelEditor(viewport, edit=True, wireframeOnShaded=False)

        return template
        
    def toggle_ui_state(self):
        for elem in [self.wireframe_box,
                    self.show_imgplane_box,
                    self.half_res_box]:
            elem.setEnabled(self.template_override_setting.isChecked())

    def validate_output_path(self,file_path):   
        path_output = Path(file_path)
        if not path_output.is_dir():
            path_output.mkdir()    
        return path_output.is_dir()
        
    def validate_output(self,file_path):   
        file_output = Path(file_path)  
        return file_output.is_file()
      
    def create_movie(self,input_sequence, output_filename, framerate, post_open=True) -> str :
 
        ffmpeg_input_string = utils.Parsing.playblast_output_to_ffmpeg_input(input_sequence)
        output_path = f'{output_filename}.mp4'
        PlayBlastPlusLogger.info(f'ffmpeg_input_string {ffmpeg_input_string}')
        PlayBlastPlusLogger.info(f'output_path {output_path}')

        encode.mp4_from_image_sequence(ffmpeg_input_string,
                                output_path, 
                                framerate=24, 
                                post_open=post_open
                            )
                            
        return output_path

    def clear_playblast_directory(self):
        utils.FolderOps.purge_contents(self.current_playblast_directory)
        PlayBlastPlusLogger.info("Playblast directory was cleared")
        
    def open_playblast_directory(self):
        utils.FolderOps.explore(self.current_playblast_directory)
        PlayBlastPlusLogger.info(f"Open Playblast Directory {self.current_playblast_directory}")
        
    def get_output_name(self, strToken) -> str:
        return tokens.format_tokens(strToken,None)
        
    def get_current_template(self) -> dict:
        """
        We want to clone the template as we might want to override the keys each time 
        we make playblast. This means the defaults are not modified direectly 
        and are collected only when init is called
        """
        selected_template = self._TEMPLATES[self.template_list.currentIndex()]
        capture_template = selected_template[self.template_list.currentText()]
        return copy.deepcopy(capture_template)
        
    def set_clipboard_data(self,filepath:str):
        data = QtCore.QMimeData()
        url = QtCore.QUrl.fromLocalFile(filepath)
        data.setUrls([url])
        return QtWidgets.QApplication.clipboard().setMimeData(data)

    def capture_viewport(self):
        
        output_path = Path (self.current_playblast_directory, 'captures') 
    
        if self.validate_output_path(output_path):
            snap_image_filename = (tokens.format_tokens(f'{output_path}\{self.tokens_field.text()}_capture',None))
            capture_template = self.get_current_template()    
            capture_template["filename"] = snap_image_filename
            
            if self.template_override_setting.isChecked():
                self.set_overrides(capture_template)

            snap_clip_image = capture.snap(**capture_template)
            PlayBlastPlusLogger.info(f"Viewport Capture saved to {snap_clip_image}")
            
            if self.copy_to_clipboard_setting.isChecked():
                    # check the mp4 has written and is a file
                    if self.validate_output(snap_clip_image):
                        self.set_clipboard_data(snap_clip_image)
                        
            if self.template_override_setting.isChecked():
                self.remove_display_layer()

 
    def create_playblast(self):

        output_name = self.get_output_name(self.tokens_field.text())
        output_path = self.current_playblast_directory

        if self.validate_output_path(output_path):

            capture_template = self.get_current_template()    
            capture_template["filename"] = Path (output_path) / output_name
            
            if self._CAMERAS:
                capture_template["camera"] = self._CAMERAS[self.camera_list.currentIndex()]

                if capture_template["frame_padding"] > 4:
                    PlayBlastPlusLogger.warning ("Playblast padding should be set to 4 to allow output transcode compatibility - This value will be set automatically.")

                if self.template_override_setting.isChecked():
                    self.set_overrides(capture_template)

                filename = capture.capture(**capture_template)
                mp4_output = self.create_movie(filename, capture_template["filename"], 24, post_open=True)
                
                # if self.clipboard_box.isChecked():
                    
                if self.copy_to_clipboard_setting.isChecked():
                    # check the mp4 has written and is a file
                    if self.validate_output(mp4_output):
                        self.set_clipboard_data(mp4_output)
                        
                # if not self.images_box.isChecked():
                if not self.keep_images_setting.isChecked():   
                    utils.FolderOps.purge_contents(output_path, ext='.png', skip_folder='captures')
                 
                if self.template_override_setting.isChecked():
                    self.remove_display_layer()

            else:
                OpenMaya.MGlobal.displayWarning("Please create a valid camera.") 
        else:
            OpenMaya.MGlobal.displayError(f'The filename specified is wrong - {output_name}') 

def kill_ui(name):
    """ Deletes an already created widget

    Args:
        name (str): the widget object name
    """

    # finds workspace control if dockable widget
    if cmds.workspaceControl(name, exists=True):
        cmds.workspaceControl(name, edit=True, clp=False)
        cmds.deleteUI(name)

    # finds the widget
    widget = OpenMayaUI.MQtUtil.findWindow(name)

    if not widget:
        return

    # wraps the widget into a qt object
    qt_object = wrapInstance(long(widget), QtWidgets.QDialog)

    # sets the widget parent to none
    qt_object.setParent(None)

    # deletes the widget
    qt_object.deleteLater()
    del(qt_object)


def run(*args):  # @unusedVariable
    """ Opens the Cache Manager UI
    """
    # UI WIDGET NAME
    
    tool = PlayblastPlusUI(UI_NAME)
    tool.show(dockable=True)
    PlayBlastPlusLogger.info("playblastPlus Running...")

run()