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
                "color: rgb(220, 250, 250);"
                "height: 40px;"
                "background-color: rgb(103, 163, 217);"
                "border:1px solid black;"
                "border-radius:4px;}"
                "QPushButton:pressed"
                "{"
                "background-color: rgb(44, 189, 218);"
                "}"
                )
    
    BUTTON_SIDEKICK = (
                "QPushButton{"
                "font: bold 12px;"
                "color: rgb(220, 250, 250);"
                "height: 40px;"
                "background-color: rgb(197, 104, 141);"
                "border:1px solid black;"
                "border-radius:4px;}"
                "}"
                "QPushButton:pressed"
                "{"
                "background-color: rgb(197, 104, 141);"
                "}"
                )
    
    TEXTFIELD = (
                "QLineEdit{"
                "font: bold 12px;"
                "color: rgb(103, 163, 217);"
                "height: 12px;"
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
                "border-radius: 1px"
                "}"
                 )
    
    PROGRESSBAR = (
                "QProgressBar {"
                "background-color: #C0C6CA;"
                "border: 0px;"
                "padding: 0px;"
                "height: 5px; // To change the progress bar height"
                "}"
                "QProgressBar::chunk {"
                "background: #7D94B0;"
                "width:5px"
                "}"
                )

    
class ToolHeader(QtWidgets.QWidget):
    """A standardised Tool Header widget, with line Logo and a 
        setter for the script name field.

    Args:
        name (str): the control name (not needed)
        text (str): The title text to be shown on the header 
    
    Returns:
        A QWdidget control item.
    
    **Useful code:**
    
    To get a visual representation of all icons loaded in Maya

    .. code-block:: python

        import maya.app.general.resourceBrowser as resourceBrowser
        resBrowser = resourceBrowser.resourceBrowser()
        path = resBrowser.run()
 
    """

    LINE_LOGO = 'tl_logo_white.png'
    STYLE_SHEET = (
                "font: bold 12px;"
                "color: rgb(205, 205, 205);"
                "background-color: rgb(30,30,30);"
                "padding:6px"
                 )

    def __init__(self, name='', text= '', parent=None):
            super(ToolHeader, self).__init__(parent)
            self.name = name
            self.headerTitle = text
            self.registerUserData = ""            
            self.setMinimumSize(QtCore.QSize(180, 40))
            # self.setMaximumSize(QtCore.QSize(500, 40))
            self.setStyleSheet(self.STYLE_SHEET)             
            self.create_widgets()
            self.create_layout()
        
    def create_widgets(self):
            
        self.labelIcon = QtWidgets.QLabel()
        self.labelIcon.setStyleSheet(self.STYLE_SHEET)          
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, 
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.labelIcon.sizePolicy().hasHeightForWidth())
        self.labelIcon.setMaximumSize(QtCore.QSize(1600, 40))
        self.labelIcon.setSizePolicy(sizePolicy) 

        self.labelText = QtWidgets.QLabel()
        self.labelText.setStyleSheet(self.STYLE_SHEET)
        self.labelText.setText(self.headerTitle)
        # self.labelText.setMaximumSize(QtCore.QSize(10000, 40)) 

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)

        # self.labelText.setSizePolicy(sizePolicy) 
        self.labelText.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)


    def create_layout(self): 
        
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName('gridLayout') 

        self.addHeaderIcon(self.labelIcon)
        
        self.gridLayout.addWidget(self.labelIcon,1,0)
        self.gridLayout.addWidget(self.labelText,1,1)
        self.setLayout(self.gridLayout) 
        
    def setTitleText(self,text):
        self.headerTitle = text 
        self.labelText.setText(self.headerTitle)

            
    def addHeaderIcon(self, widget):
        icon_root = settings.get_resources_directory()
            
        if icon_root:
            # image_path = os.path.join (icon_root,self.LINE_LOGO)
            image_path = Path(icon_root , self.LINE_LOGO )
            image = QtGui.QImage(str(image_path))
            pixmap = QtGui.QPixmap()
            pixmap.convertFromImage(image)
            widget.setPixmap(pixmap)

    def iconClicked(self):
        pass

class Downloader(QtCore.QThread):
    """
    A thread that downloads the data from the server. This is done in a separate thread so that the GUI can remain responsive.
    @param parent - the parent object, which is the GUI itself.
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
    The window that allows the user to download the data. This window is used to download the data from the server.
    """

    
    def __init__(self, url:str, locations:list=[], parent=None):
        super(DownloadWindow, self).__init__(parent)
        self.setWindowTitle(" ")
        self.resize(300,100)
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
                                    "it's a requirement to install ffmpeg.exe"
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

        main_layout.setMargin(8)
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

        