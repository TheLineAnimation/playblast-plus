"""
Playblast Plus

A huge thanks to Jerome Dresse for his UI code from SmearDeform.
I used this (and some other snippets from mGear) to help speed up development
www.nodilus.lu

"""

# Globals
import copy
from typing import Union
from pathlib import Path
from playblast_plus import (
    PLAYBLAST_PLUS_MODULE_ROOT as module_root,
    version
)
from playblast_plus.lib import (
    utils as utils,
    widgets,
    settings,
    preset,
    encode
)
from playblast_plus.vendor.Qt import (
    QtWidgets,
    QtGui,
    QtCore
)
from playblast_plus.lib import logger
from playblast_plus.lib.dcc import Host
UI_NAME = "playblast_plus_dialog"


# custom imports


# standard lib imports

HOST = Host()
UI_BASECLASS = HOST.UIBASECLASS


class PlayBlastPlusLogger(logger.Logger):
    """
    Set up a custom script logger
    """
    LOGGER_NAME = "PlayBlastPlusLogger"


class PlayblastPlusUI(UI_BASECLASS):
    """
    PlayBlastPlus User Interface
    """
    # CLASS LEVEL GLOBALS
    WF_OVERRIDE_LAYER_NAME = 'pbp_Wireframe_Override'
    ISOLATE_SET_NAME = 'pbp_isolate'

    def __init__(self, host: Host):
        super(PlayblastPlusUI, self).__init__(parent=host.main_window)
        self.host = host

        # sets title and object name
        self.setWindowTitle(" ")
        self.setObjectName(UI_NAME)
        self.setWindowFlags(QtCore.Qt.Tool)

        self.setMinimumWidth(250)

        self._TEMPLATES = {}
        self._CAMERAS = self.host.scene.get_scene_cameras()

        # creates main layout widget
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # PySide2 depreciated the setMargin call
        if hasattr(self.main_layout, "setMargin"):
            self.main_layout.setMargin(2)
        else:
            self.main_layout.setContentsMargins(2, 2, 2, 2)

        self.main_layout.setSpacing(6)

        self.main_layout.setAlignment(QtCore.Qt.AlignTop)

        self._create_actions()

        # call the widget creation method
        self._create_widgets()
        # connects signals
        self._connect_signals()

        # Get the scene cameras first, we will need to see
        # if the last camera used can be set automatically

        self.camera_list.clear()
        # SORT THE CAMERAS FUNCTION OUT IN BOTH HOSTS
        self.camera_list.addItems(self._CAMERAS)

        # populate the UI with data
        self.host_settings_directory = self.host.scene.get_user_directory()
        self.current_playblast_directory = self.host.scene.get_output_dir()

        self._CONFIG = settings.get_config()
        PlayBlastPlusLogger.info(f'Configuration settings { self._CONFIG }')

        self._TEMPLATES = preset.load_templates([str(module_root /
                                                    self._CONFIG['studio_templates'])])

        # to identify the different presets, they are stored within a
        # dictionary, so the first key is the name identifier
        template_names = [list(k.keys())[0] for k in self._TEMPLATES]
        # PlayBlastPlusLogger.info(template_names)
        self.template_list.addItems(template_names)

        self._SETTINGS = self._load_host_settings()
        PlayBlastPlusLogger.info(f'{self.host.name} settings {self._SETTINGS}')

        if not self._SETTINGS['output_token']:
            self.tokens_field.setText(self._CONFIG['default_output_token'])
        else:
            self.tokens_field.setText(self._SETTINGS['output_token'])

        PlayBlastPlusLogger.info(
            f'Current Playblast Directory : {self.current_playblast_directory}'
        )

        self.toggle_ui_state()

        self.host.preview.pre_process(isolate_set_name=self.ISOLATE_SET_NAME)

    def CloseEvent(self, event):
        self._save_host_settings(self.host_settings_directory)
        PlayBlastPlusLogger.info(
            f'Settings saved to : {self.host_settings_directory}')
        event.accept()

    def _connect_signals(self):
        """
        Connects widget signals to functionalities
        """
        self.playblast_button.clicked.connect(self.create_playblast)
        self.camera_refresh.clicked.connect(self.refresh_camera_list)
        self.capture_button.clicked.connect(self.capture_viewport)
        self.open_playblast_dir.triggered.connect(
            self.open_playblast_directory)
        self.open_last_playblast.triggered.connect(self.open_last_capture)
        self.purge_playblast_dir.triggered.connect(
            self.clear_playblast_directory)
        self.template_override_setting.toggled.connect(self.toggle_ui_state)
        self.camera_list.currentIndexChanged.connect(self.camera_list_changed)
        self.closeEvent = self.CloseEvent

    def _create_actions(self):

        self.copy_to_clipboard_setting = QtWidgets.QAction(
            "Copy To Clipboard", self)
        self.copy_to_clipboard_setting.setCheckable(True)
        self.copy_to_clipboard_setting.setChecked(True)

        self.add_burnin_setting = QtWidgets.QAction("Add Burnin", self)
        self.add_burnin_setting.setCheckable(True)
        self.add_burnin_setting.setChecked(False)

        self.keep_images_setting = QtWidgets.QAction(
            "Keep Intermediate Images", self)
        self.keep_images_setting.setCheckable(True)
        self.keep_images_setting.setChecked(False)

        self.template_override_setting = QtWidgets.QAction("Enable", self)
        self.template_override_setting.setCheckable(True)
        self.template_override_setting.setChecked(False)

        self.use_workspace_setting = QtWidgets.QAction("Use Workspace", self)
        self.use_workspace_setting.setCheckable(True)
        self.use_workspace_setting.setChecked(False)

    def _create_widgets(self):
        """ Creates the widget elements the user will interact with
        """
        self.menu_bar = QtWidgets.QMenuBar()
        self.display_menu = self.menu_bar.addMenu("Settings")

        version_separator = QtWidgets.QLabel(
            f'<b>{self.host.UITEXT_preview} Plus v{version.version}</b>')
        version_separator_action = QtWidgets.QWidgetAction(self)
        version_separator_action.setDefaultWidget(version_separator)
        self.display_menu.addAction(version_separator_action)

        self.open_last_playblast = QtWidgets.QAction("Open Last Capture", self)
        self.open_last_playblast.setIcon(widgets.Icons.get("video"))

        self.display_menu.addAction(self.open_last_playblast)

        self.open_playblast_dir = QtWidgets.QAction(
            f"Explore {self.host.UITEXT_preview} Folder", self)
        self.open_playblast_dir.setIcon(widgets.Icons.get("folder"))

        self.display_menu.addAction(self.open_playblast_dir)
        self.display_menu.addAction(self.use_workspace_setting)

        self.purge_playblast_dir = QtWidgets.QAction(
            f"Empty {self.host.UITEXT_preview} Folder", self)
        self.purge_playblast_dir.setIcon(widgets.Icons.get("bin"))

        folder_separator = QtWidgets.QLabel("<b>Template Overrides</b>")
        folder_separator_action = QtWidgets.QWidgetAction(self)
        folder_separator_action.setDefaultWidget(folder_separator)
        self.display_menu.addAction(folder_separator_action)
        self.display_menu.addAction(self.template_override_setting)

        folder_separator = QtWidgets.QLabel("<b>File Options</b>")
        folder_separator_action = QtWidgets.QWidgetAction(self)
        folder_separator_action.setDefaultWidget(folder_separator)
        self.display_menu.addAction(folder_separator_action)

        self.display_menu.addAction(self.add_burnin_setting)
        self.display_menu.addAction(self.copy_to_clipboard_setting)

        folder_separator = QtWidgets.QLabel("<b>Housekeeping</b>")
        folder_separator_action = QtWidgets.QWidgetAction(self)
        folder_separator_action.setDefaultWidget(folder_separator)
        self.display_menu.addAction(folder_separator_action)

        self.display_menu.addAction(self.keep_images_setting)
        self.display_menu.addAction(self.purge_playblast_dir)

        # creates full frame border around the entire UI
        # self.main_layout is the container for the entire UI
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(7)
        frame_layout = QtWidgets.QVBoxLayout(frame)

        # PySide2 depreciated the setMargin call
        if hasattr(frame_layout, "setMargin"):
            frame_layout.setMargin(4)
        else:
            frame_layout.setContentsMargins(4,4,4,4)

        frame_layout.setSpacing(4)

        main_layout = QtWidgets.QGridLayout(frame)

        # bold font for the heading labels
        custom_font = QtGui.QFont()
        custom_font.setBold(False)

        # Add widgets to the layout
        # ToolHeader is a custom label widget imported from lib.widgets
        header = widgets.ToolHeader(
            'pbp_header', f'{self.host.UITEXT_preview.upper()} PLUS ')

        cam_formlayout = QtWidgets.QGridLayout()

        # PySide2 depreciated the setMargin call
        if hasattr(cam_formlayout, "setMargin"):
            cam_formlayout.setMargin(0)
        else:
            cam_formlayout.setContentsMargins(0,0,0,0)


        template_label = QtWidgets.QLabel("Capture Template")
        template_label.setFont(custom_font)

        self.template_list = QtWidgets.QComboBox()

        cam_formlayout.addWidget(template_label)
        cam_formlayout.addWidget(self.template_list)

        self.camera_list = QtWidgets.QComboBox()

        self.folder_icon = QtWidgets.QLabel()
        self.folder_icon.setPixmap(QtGui.QPixmap(":/folder-open.png"))
        self.folder_icon.setMaximumWidth(16)

        self.imageplane_icon = QtWidgets.QLabel()
        self.imageplane_icon.setPixmap(QtGui.QPixmap(":/ImagePlane.png"))
        self.imageplane_icon.setMaximumWidth(16)

        self.half_res_icon = QtWidgets.QLabel()
        self.half_res_icon.setPixmap(QtGui.QPixmap(":/imageDisplay.png"))
        self.half_res_icon.setMaximumWidth(16)

        self.isolate_icon = QtWidgets.QLabel()
        self.isolate_icon.setPixmap(QtGui.QPixmap(":/IsolateSelected.png"))
        self.isolate_icon.setMaximumWidth(16)

        self.wireframe_icon = QtWidgets.QLabel()
        self.wireframe_icon.setPixmap(QtGui.QPixmap(":/WireFrameOnShaded.png"))
        self.wireframe_icon.setMaximumWidth(16)

        self.tokens_field = QtWidgets.QLineEdit()

        style = widgets.Styles.TEXTFIELD
        self.tokens_field.setStyleSheet(style)

        self.tokens_field.setToolTip("""
        <b>Output Tokens</b><br>You can use special <b>&lt;value&gt;</b>
        notation here:<br><i>&lt;scene&gt;<br>&lt;user&gt;<br>
        &lt;camera&gt;</i><br>These will act like variables
        and will be swapped for the relevant value.
        """
                                     )

        # create
        style = widgets.Styles.BUTTON_HERO
        self.playblast_button = QtWidgets.QPushButton(
            self.host.UITEXT_preview.upper())
        self.playblast_button.setStyleSheet(style)

        # edit frame border and layout
        edit_frame = QtWidgets.QFrame()
        edit_frame.setFrameStyle(6)
        locations_layout = QtWidgets.QGridLayout(edit_frame)

        # PySide2 depreciated the setMargin call
        if hasattr(locations_layout, "setMargin"):
            locations_layout.setMargin(4)
        else:
            locations_layout.setContentsMargins(4,4,4,4)
        
        locations_layout.setSpacing(4)

        # reset
        style = widgets.Styles.BUTTON_SIDEKICK
        self.capture_button = QtWidgets.QPushButton("SNAP")
        self.capture_button.setStyleSheet(style)

        # Overides
        overrides_frame = QtWidgets.QFrame()
        overrides_frame.setFrameStyle(6)

        overrides_layout = QtWidgets.QGridLayout(overrides_frame)
        overrides_layout.setColumnStretch(1, 4)

        self.wireframe_box = QtWidgets.QCheckBox("Show Wireframe")
        self.wireframe_box.setChecked(False)

        self.show_imgplane_box = QtWidgets.QCheckBox(
            f"Show {self.host.UITEXT_image_plane}")
        self.show_imgplane_box.setChecked(False)

        self.half_res_box = QtWidgets.QCheckBox("Half Res")
        self.half_res_box.setChecked(False)

        self.isolate_box = QtWidgets.QCheckBox("Only show pbp_isolate set")
        self.isolate_box.setChecked(False)

        overrides_label = QtWidgets.QLabel("Template Overrides")
        overrides_label.setFont(custom_font)

        overrides_layout.addWidget(overrides_label, 0, 0, 1, 5)

        overrides_layout.addWidget(self.imageplane_icon, 1, 0, 1, 1)
        overrides_layout.addWidget(self.show_imgplane_box, 1, 1, 1, 1)

        overrides_layout.addWidget(self.wireframe_icon, 2, 0, 1, 1)
        overrides_layout.addWidget(self.wireframe_box, 2, 1, 1, 1)

        overrides_layout.addWidget(self.isolate_icon, 3, 0, 1, 1)
        overrides_layout.addWidget(self.isolate_box, 3, 1, 1, 1)

        overrides_layout.addWidget(self.half_res_icon, 4, 0, 1, 1)
        overrides_layout.addWidget(self.half_res_box, 4, 1, 1, 1)

        locations_label = QtWidgets.QLabel("Output Name")
        locations_label.setFont(custom_font)

        locations_layout.addWidget(locations_label, 0, 0, 1, 1)
        locations_layout.addWidget(self.tokens_field, 1, 0, 1, 4)

        capture_frame = QtWidgets.QFrame()
        capture_frame.setFrameStyle(6)


        # camera refresh
        self.camera_refresh = QtWidgets.QPushButton("Refresh")

        capture_layout = QtWidgets.QGridLayout(capture_frame)

        camera_label = QtWidgets.QLabel("Camera")
        camera_label.setFont(custom_font)

        # PySide2 depreciated the setMargin call
        if hasattr(capture_layout, "setMargin"):
            capture_layout.setMargin(4)
        else:
            capture_layout.setContentsMargins(4, 4, 4, 4)

        capture_layout.setSpacing(4)

        capture_layout.addWidget(camera_label, 0, 0, 1, 1)

        capture_layout.addWidget(self.camera_list, 1, 0, 1, 3)
        capture_layout.addWidget(self.camera_refresh, 1, 3, 1, 1)
       
        capture_layout.addWidget(self.playblast_button, 2, 0, 1, 3)
        capture_layout.addWidget(self.capture_button, 2, 3, 1, 1)

        # add widgets to layouts
        self.main_layout.addWidget(header)
        self.main_layout.setMenuBar(self.menu_bar)

        self.main_layout.addWidget(frame)
        frame_layout.addLayout(cam_formlayout)
        frame_layout.addWidget(overrides_frame)
        frame_layout.addWidget(edit_frame)
        frame_layout.addWidget(capture_frame)

    def _save_host_settings(self, path):
        ui_dict = self._SETTINGS
        ui_dict['toggle_overrides'] = self.template_override_setting.isChecked()
        ui_dict['toggle_copy'] = self.copy_to_clipboard_setting.isChecked()
        ui_dict['toggle_keep'] = self.keep_images_setting.isChecked()
        ui_dict['set_imageplane'] = self.show_imgplane_box.isChecked()
        ui_dict['set_wire'] = self.wireframe_box.isChecked()
        ui_dict['isolate'] = self.isolate_box.isChecked()
        ui_dict['set_half'] = self.half_res_box.isChecked()
        ui_dict['output_token'] = self.tokens_field.text()
        ui_dict['last_camera'] = self.camera_list.currentText()
        ui_dict['last_template'] = self.template_list.currentText()
        ui_dict['use_workspace'] = self.use_workspace_setting.isChecked()
        ui_dict['add_burnin'] = self.add_burnin_setting.isChecked()

        settings.save_host_settings(path, self._SETTINGS)

    def _load_host_settings(self):

        PlayBlastPlusLogger.info(
            f'{self.host.name} settings directory { self.host_settings_directory }')

        settings_dict = settings.get_host_settings(
            self.host_settings_directory)

        self.template_override_setting.setChecked(
            settings_dict['toggle_overrides'])
        self.copy_to_clipboard_setting.setChecked(settings_dict['toggle_copy'])
        self.keep_images_setting.setChecked(settings_dict['toggle_keep'])
        self.show_imgplane_box.setChecked(settings_dict['set_imageplane'])
        self.wireframe_box.setChecked(settings_dict['set_wire'])
        self.half_res_box.setChecked(settings_dict['set_half'])
        self.tokens_field.setText(settings_dict['output_token'])
        self.use_workspace_setting.setChecked(settings_dict['use_workspace'])
        self.add_burnin_setting.setChecked(settings_dict['add_burnin'])
        self.isolate_box.setChecked(settings_dict['isolate'])

        index = self.camera_list.findText(
            settings_dict['last_camera'], QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.camera_list.setCurrentIndex(index)

        if 'last_template' in settings_dict:
            index = self.template_list.findText(
                settings_dict['last_template'], QtCore.Qt.MatchFixedString)
            print(f'template index : {index}')
            if index >= 0:
                self.template_list.setCurrentIndex(index)
        else:
            PlayBlastPlusLogger.info(
                f'{self.host.name} The last template setting key wasn\'t found but it will be added.')

        return settings_dict

    def set_template_overrides(self, template) -> dict:

        height, width = self.host.scene.get_render_resolution(0.5)

        self.host.preview.set_override_properties(
            template_override_setting=self.template_override_setting.isChecked(),
            wireframe_option=self.wireframe_box.isChecked(),
            half_res_option=self.half_res_box.isChecked(),
            image_plane_option=self.show_imgplane_box.isChecked(),
            isolate_option=self.isolate_box.isChecked(),
            override_layer_name=self.WF_OVERRIDE_LAYER_NAME,
            wireframe_color=self._CONFIG['overrides']['wireframe_color'],
            render_height=height,
            render_width=width,
            template=template
        )

    def toggle_ui_state(self):
        for elem in [self.wireframe_box,
                     self.show_imgplane_box,
                     self.half_res_box,
                     self.imageplane_icon,
                     self.half_res_icon,
                     self.wireframe_icon,
                     self.isolate_icon,
                     self.isolate_box,
                     ]:

            elem.setEnabled(self.template_override_setting.isChecked())

    def validate_output_path(self, file_path):
        path_output = Path(file_path)
        if not path_output.is_dir():
            path_output.mkdir()
        return path_output.is_dir()

    def validate_output(self, file_path):
        file_output = Path(file_path)
        return file_output.is_file()

    def create_movie(self, ffmpeg_input_string,
                     output_filename,
                     post_open=True
                     ) -> str:

        output_path = f'{output_filename}.mp4'
        current_fr = self.host.scene.getFrameRate()
        framerange = self.host.scene.getFrameRange()
        burnin_str = self.get_output_name(self.tokens_field.text())

        PlayBlastPlusLogger.info(f'output_path {output_path}')

        if self._SETTINGS['custom_viewer']:
            viewer_start_path = self._SETTINGS['custom_viewer']
        else:
            viewer_start_path = 'start'

        encode.mp4_from_image_sequence(ffmpeg_input_string,
                                       output_path,
                                       framerate=current_fr,
                                       start_frame=int(framerange[0]),
                                       end_frame=int(
                                           framerange[1]-framerange[0]+1),
                                       add_burnin=self.add_burnin_setting.isChecked(),
                                       burnin_text=burnin_str,
                                       post_open=post_open,
                                       viewer_arg=viewer_start_path,
                                       )

        return output_path

    def clear_playblast_directory(self):
        utils.FolderOps.purge_contents(self.current_playblast_directory)
        PlayBlastPlusLogger.info("Playblast directory was cleared")

    def open_playblast_directory(self):
        utils.FolderOps.explore(self.current_playblast_directory)
        PlayBlastPlusLogger.info(
            f"Open Playblast Directory {self.current_playblast_directory}"
        )

    def open_last_capture(self):
        # file should be current to the settings dictionary
        # as it's saved to this before writing out to JSON each time
        last_captured = self._SETTINGS['last_playblast']
        if self.validate_output(last_captured):
            if self._SETTINGS['custom_viewer']:
                encode.open_media_file(
                    last_captured, self._SETTINGS['custom_viewer'])
            else:
                encode.open_media_file(last_captured)

        PlayBlastPlusLogger.info(
            f"Launching last captured : {self.current_playblast_directory}"
        )

    def update_last_playblast(self, filepath):
        self._SETTINGS['last_playblast'] = filepath
        self._save_host_settings(self.host_settings_directory)

    def get_output_name(self, strToken) -> str:
        return self.host.tokens.format_tokens(strToken, None)

    def get_current_template(self) -> dict:
        """
        We want to clone the template as we might want to override the keys 
        each time we make playblast. This means the defaults are not modified 
        directly and are collected only when init is called
        """
        selected_template = self._TEMPLATES[self.template_list.currentIndex()]
        capture_template = selected_template[self.template_list.currentText()]
        return copy.deepcopy(capture_template)

    def set_clipboard_data(self, filepath: str):
        data = QtCore.QMimeData()
        url = QtCore.QUrl.fromLocalFile(filepath)
        data.setUrls([url])
        return QtWidgets.QApplication.clipboard().setMimeData(data)

    def capture_viewport(self):
        pass
        # self.host.preview.create()

        output_path = Path(self.current_playblast_directory, 'captures')
        # output_name = self.get_output_name(self.tokens_field.text())
        # output_path = self.current_playblast_directory
        #
        if self.validate_output_path(output_path):
            snap_image_filename = (self.host.tokens.format_tokens(
                f'{output_path}\{self.tokens_field.text()}_capture', None))
            capture_template = self.get_current_template()

            capture_template["filename"] = snap_image_filename

            if self._CAMERAS:
                capture_template["camera"] = \
                    self._CAMERAS[self.camera_list.currentIndex()]

            if self.template_override_setting.isChecked():
                self.set_template_overrides(capture_template)

            snap_clip_image = self.host.preview.snapshot(
                template=capture_template,
                host_options=self._SETTINGS
            )

            PlayBlastPlusLogger.info(
                f"Viewport Capture saved to {snap_clip_image}")

            self.update_last_playblast(snap_clip_image)

            if self.copy_to_clipboard_setting.isChecked():
                # check the mp4 has written and is a file
                if self.validate_output(snap_clip_image):
                    self.set_clipboard_data(snap_clip_image)

            if self.template_override_setting.isChecked():
                self.host.preview.post_process(
                    wireframe_option=self.wireframe_box.isChecked(),
                    override_layer_name=self.WF_OVERRIDE_LAYER_NAME,
                )

    def refresh_camera_list(self):
        current_camera = self.camera_list.currentText()

        self.camera_list.clear()
        self._CAMERAS = self.host.scene.get_scene_cameras()
        self.camera_list.addItems(self._CAMERAS)

        if current_camera in self._CAMERAS:
            index = self.camera_list.findText(current_camera)
        else:
            index = 0 
        self.camera_list.setCurrentIndex(index)

    def camera_list_changed(self):
        PlayBlastPlusLogger.info(
            f"Set Camera {self._CAMERAS[self.camera_list.currentIndex()]}")   

        self.host.scene.set_viewport_camera(
            self._CAMERAS[self.camera_list.currentIndex()]
        )

    def create_playblast(self):

        output_name = self.get_output_name(self.tokens_field.text())
        output_path = self.current_playblast_directory

        if self.validate_output_path(output_path):

            capture_template = self.get_current_template()
            capture_template["filename"] = Path(output_path) / output_name

            if self._CAMERAS:
                capture_template["camera"] = \
                    self._CAMERAS[self.camera_list.currentIndex()]

                if capture_template["frame_padding"] > 4:
                    PlayBlastPlusLogger.warning("""Playblast padding 
                            "should be set to 4 to allow output transcode " \
                            "compatibility - This value will be set " \
                            "automatically."""
                                                )

                if self.template_override_setting.isChecked():
                    self.set_template_overrides(capture_template)

                filename = self.host.preview.create(template=capture_template,
                                                    host_options=self._SETTINGS
                                                    )
                PlayBlastPlusLogger.info(
                    f"filename {filename}")

                mp4_output = self.create_movie(
                    filename,
                    capture_template["filename"],
                    post_open=True
                )

                if self.validate_output(mp4_output):
                    self.update_last_playblast(mp4_output)

                if self.copy_to_clipboard_setting.isChecked():
                    # check the mp4 has written and is a file
                    if self.validate_output(mp4_output):
                        self.set_clipboard_data(mp4_output)

                # if not self.images_box.isChecked():
                if not self.keep_images_setting.isChecked():
                    utils.FolderOps.purge_contents(output_path,
                                                   ext='.png',
                                                   skip_folder='captures')

                if self.template_override_setting.isChecked():
                    self.host.preview.post_process(
                        wireframe_option=self.wireframe_box.isChecked(),
                        override_layer_name=self.WF_OVERRIDE_LAYER_NAME,
                    )

            else:
                self.host.preview.notify_user(
                    "Please create a valid camera.")
        else:
            self.host.scene.warning_message(
                f'The filename specified is wrong - {output_name}')


def run(**kwargs):  # @unusedVariable
    """
    Opens the Playblast Plus UI
    """
    PlayBlastPlusLogger.info(f'{kwargs["version"]}')

    if HOST:
        tool = PlayblastPlusUI(host=HOST)
        tool.show()
        PlayBlastPlusLogger.info(
            f"PlayblastPlus {kwargs['version'].version} {HOST} Running...")
    else:
        PlayBlastPlusLogger.info(
            f"PlayblastPlus Host environment not present or supported..")


if __name__ == "__main__":
    run()
