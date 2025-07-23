# from PySide2 import QtCore
# from PySide2 import QtGui
# from PySide2 import QtWidgets

from ..vendor.Qt import QtCore, QtGui, QtWidgets, QtSvg

from urllib.request import urlopen
from pathlib import Path
from . import settings, utils

class Icons():

    def get(icon, size=24):
        """
        Adapted from MGear > core > pyqt > get_icon
        Thanks Miguel and team for saving me endless time with your 
        method to get svg icon from the resources folder as a pixel map.

        For Maya - run this code to see internal icons

        .. code-block:: python
        
        import maya.app.general.resourceBrowser as resourceBrowser
        resBrowser = resourceBrowser.resourceBrowser()
        path = resBrowser.run()

        """
        svg_path = str(Path(settings.get_resources_directory(), f'{icon}.svg'))
        svg_renderer = QtSvg.QSvgRenderer(svg_path)
        image = QtGui.QImage(size, size, QtGui.QImage.Format_ARGB32)
        # Set the ARGB to 0 to prevent rendering artifacts
        image.fill(0x00000000)
        svg_renderer.render(QtGui.QPainter(image))
        pixmap = QtGui.QPixmap.fromImage(image)
        return pixmap

class Styles():
    """
    Seems to be better form to write multi-line strings without 
    escape characters, as it doesn't destroy formatting and conforms with PEP-8
    """
    CHECKBOX = (
                "QCheckBox {"
                "background-color: #3C3C3C;"
                "}"
                "QWidget {"
                "background-color: #3C3C3C;"
                "}"
                )
    
    BUTTON_HERO = (
                "QPushButton{"
                "font: bold 12px;"
                "color: #f8f8f8;"
                "height: 40px;"
                "}"
                "QPushButton:pressed"
                "{"
                "background-color: #fa391f;"
                "}"
                )
    
    BUTTON_SIDEKICK = (
                "QPushButton{"
                "font: bold 12px;"
                "color: #f8f8f8;"
                "height: 40px;"
                "}"
                "}"
                "QPushButton:pressed"
                "{"
                "background-color: #fa391f;"
                "}"
                )
    
    BUTTON_TOOL = (
                "QPushButton{"
                "font: bold 12px;"
                "color: #f8f8f8;"
                "height: 16px;"
                "}"
                "}"
                "QPushButton:pressed"
                "{"
                "background-color: #fa391f;"
                "}"
                )
    
    TEXTFIELD = (
                "QLineEdit{"
                "font: bold 12px;"
                "color: #fa391f;"
                "height: 16px;"
                "}"
                )
    
    LABEL_PATH = (
                "QLabel{"
                "font: bold 10px;"
                "color: #333300;"
                "background-color: #cccc99;"
                "border-style: solid;"
                "border-width: 1px;"
                "border-color: rgb(125, 125, 125);;"
                "}"
                 )
    
    PROGRESSBAR = (
                "QProgressBar {"
                "background-color: #0c0c0c;"
                "border: 0px;"
                "padding: 0px;"
                "height: 5px; // To change the progress bar height"
                "}"
                "QProgressBar::chunk {"
                "background: #fa391f;"
                "width:5px"
                "}"
                )

class ToolHeader(QtWidgets.QWidget):
    """A standardized Tool Header widget with a scalable logo."""

    LINE_LOGO = 'tl_logo_white.png'
    STYLE_SHEET = (
        "font: bold 12px;"
        "color: #f8f8f8;"
        "background-color: #fa391f;"
        "padding:2px"
    )

    MIN_ICON_WIDTH = 24  
    max_icon_width = None

    def __init__(self, name='', text='', parent=None):
        super(ToolHeader, self).__init__(parent)
        self.name = name
        self.headerTitle = text
        self.registerUserData = ""
        self.setMinimumSize(QtCore.QSize(180, 40))
        self.setStyleSheet(self.STYLE_SHEET)
        self.icon_pixmap = None  # Store original image

        self.create_widgets()
        self.create_layout()
        self.create_actions()
        self.loadHeaderIcon()  # Load the initial icon

    def create_widgets(self):
        self.labelIcon = ClickableLabel()
        self.labelIcon.setStyleSheet(self.STYLE_SHEET)
        self.labelIcon.setMaximumHeight(40)  # Keep height fixed

        self.labelText = ClickableLabel()
        self.labelText.setStyleSheet(self.STYLE_SHEET)
        self.labelText.setText(self.headerTitle)
        self.labelText.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

    def create_layout(self):
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)

        self.gridLayout.addWidget(self.labelIcon, 1, 0)
        self.gridLayout.addWidget(self.labelText, 1, 1)
        self.setLayout(self.gridLayout)

    def create_actions(self):
        self.labelIcon.clicked.connect(self.iconClicked)
        self.labelText.clicked.connect(self.iconClicked)

    def iconClicked(self):
        import webbrowser
        webbrowser.open(settings.get_doclink())

    def setTitleText(self, text):
        self.headerTitle = text
        self.labelText.setText(self.headerTitle)

    def resizeEvent(self, event):
        """Resize the icon dynamically when the widget resizes."""
        super(ToolHeader, self).resizeEvent(event)
        self.updateHeaderIcon()

    def loadHeaderIcon(self):
        """Load the header icon and determine the max size."""
        icon_root = settings.get_resources_directory()
        if not icon_root:
            return

        image_path = Path(icon_root, self.LINE_LOGO)
        image = QtGui.QImage(str(image_path))

        if image.isNull():
            return  # Prevent errors if image loading fails

        pixmap = QtGui.QPixmap.fromImage(image)

        # Store original pixmap and set max width
        self.icon_pixmap = pixmap
        self.max_icon_width = pixmap.width()

        self.updateHeaderIcon()  # Apply the initial size

    def updateHeaderIcon(self):
        """Resize the icon down but never scale up or below the minimum width."""
        if not self.icon_pixmap or self.max_icon_width is None:
            return

        # Determine new width within min/max range
        new_width = max(self.MIN_ICON_WIDTH, min(self.labelIcon.width(), self.max_icon_width))

        # Scale while maintaining aspect ratio
        scaled_pixmap = self.icon_pixmap.scaled(
            new_width, 40, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )

        self.labelIcon.setPixmap(scaled_pixmap)

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.Signal()

    def mouseReleaseEvent(self, ev):
        self.clicked.emit()
class Downloader(QtCore.QThread):
    """
    A thread that downloads the data from the server. This is done in a separate thread so that the GUI can remain responsive.
    """

    # Signal for the window to establish the maximum value
    # of the progress bar.
    setTotalProgress = QtCore.Signal(int)
    # Signal to increase the progress.
    setCurrentProgress = QtCore.Signal(int)
    # Signal to be emitted when the file has been downloaded successfully.
    succeeded = QtCore.Signal()

    def __init__(self, url, filename):
        super().__init__()
        self._url = url
        self._filename = filename

    def run(self):
        url = self._url
        filename =  str(Path.home() / self._filename)
        readBytes = 0
        chunkSize = 1024
        # Open the URL address.
        with urlopen(url) as r:
            # Tell the window the amount of bytes to be downloaded.
            self.setTotalProgress.emit(int(r.info()["Content-Length"]))
            with open(filename, "wb") as f:
                while True:
                    # Read a piece of the file we are downloading.
                    chunk = r.read(chunkSize)
                    # If the result is `None`, that means data is not
                    # downloaded yet. Just keep waiting.
                    if chunk is None:
                        continue
                    # If the result is an empty `bytes` instance, then
                    # the file is complete.
                    elif chunk == b"":
                        break
                    # Write into the local file the downloaded chunk.
                    f.write(chunk)
                    readBytes += chunkSize
                    # Tell the window how many bytes we have received.
                    self.setCurrentProgress.emit(readBytes)
        # If this line is reached then no exception has ocurred in
        # the previous lines.
        self.succeeded.emit()


class DownloadWindow(QtWidgets.QDialog):
    """
    The window that allows the user to download ffmpeg executable specified 
    in the config file.
    """

    def __init__(self, url:str, locations:list=[], parent=None):
        super(DownloadWindow, self).__init__(parent)
        self.setWindowTitle(" ")
        self.resize(360,100)
        self._url = url
        self._filename = str(Path(url).name)
        self._locations = locations

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.header = ToolHeader('pbp_header', 'Download Required ')  
        self.label = QtWidgets.QLabel(
                                    "To keep mp4 encoding lighting-fast, "
                                    "it's a requirement to install ffmpeg.exe "
                                    "somewhere on your local system. "
                                    "You don't appear to have FFMpeg installed "
                                    "in any of the config locations."
                                    )
        self.label.setWordWrap(True)
        self.location_widgets = []
        for l in self._locations:
            label = QtWidgets.QLabel(f'{l}')
            label.setStyleSheet(Styles.LABEL_PATH)
            self.location_widgets.append(label)

        self.label_action = QtWidgets.QLabel(
                                    "Press the button below and when complete, "
                                    "extract the zip and copy ffmpeg.exe to "
                                    "any of the folders mentioned above."
                                    )
        self.label_action.setWordWrap(True)
        
        self.button = QtWidgets.QPushButton("Start download")
        self.button.setStyleSheet(Styles.BUTTON_HERO)
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setStyleSheet(Styles.PROGRESSBAR)
        
    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)

        # PySide2 depreciated the setMargin call
        if hasattr(main_layout, "setMargin"):
            main_layout.setMargin(8)
        else:
            main_layout.setContentsMargins(8, 8, 8, 8)

        main_layout.setSpacing(8)

        main_layout.addWidget(self.header)
        main_layout.addWidget(self.label)

        if self.location_widgets:
            for each in self.location_widgets:
                main_layout.addWidget(each)

        main_layout.addWidget(self.label_action)
        main_layout.addWidget(self.button)
        main_layout.addWidget(self.progressBar)


    def create_connections(self):
        self.button.pressed.connect(self.initDownload)

    def initDownload(self):
        self.button.setText("Downloading file...")
        # Disable the button while the file is downloading.
        self.button.setEnabled(False)
        # Run the download in a new thread.
        self.downloader = Downloader(self._url, self._filename)
        # Connect the signals which send information about the download
        # progress with the proper methods of the progress bar.
        self.downloader.setTotalProgress.connect(self.progressBar.setMaximum)
        self.downloader.setCurrentProgress.connect(self.progressBar.setValue)
        # Qt will invoke the `succeeded()` method when the file has been
        # downloaded successfully and `downloadFinished()` when the
        # child thread finishes.
        self.downloader.succeeded.connect(self.downloadSucceeded)
        self.downloader.finished.connect(self.downloadFinished)
        self.downloader.start()

    def downloadSucceeded(self):
        # Set the progress at 100%.
        self.progressBar.setValue(self.progressBar.maximum())
        self.button.setText("The file has been downloaded!")
        # self.button.setVisible(False)

    def downloadFinished(self):

        utils.FolderOps.explore(str(Path.home()))
        # Delete the thread when no longer needed.
        del self.downloader

        