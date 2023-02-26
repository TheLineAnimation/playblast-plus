from urllib.request import urlopen

from playblast_plus.vendor.Qt import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

from playblast_plus.lib import widgets, utils, settings

def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

import sys
from pathlib import Path

FFMPEG_URL = settings.get_ffmpeg_download_url()
FFMPEG_FILENAME = Path(FFMPEG_URL).name

class Downloader(QtCore.QThread):

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
        url = FFMPEG_URL
        filename =  str(Path.home() / FFMPEG_FILENAME)
        readBytes = 0
        chunkSize = 1024
        # Open the URL address.
        with urlopen(url) as r:
            # Tell the window the amount of bytes to be downloaded.
            self.setTotalProgress.emit(int(r.info()["Content-Length"]))
            with open(filename, "ab") as f:
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
    def __init__(self, parent=maya_main_window()):
        super(DownloadWindow, self).__init__(parent)
        self.setWindowTitle(" ")
        self.resize(300,100)
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.header = widgets.ToolHeader('pbp_header', 'Get FFMpeg')  
        self.label = QtWidgets.QLabel("You don't appear to have FFMpeg installed in the locations specified.\n\nPress the button to start downloading.", self)
        self.label.setGeometry(20, 20, 200, 25)
        self.button = QtWidgets.QPushButton("Start download", self)

        self.progressBar = QtWidgets.QProgressBar(self)
        # self.progressBar.setGeometry(10, 115, 300, 10)
        
    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)

        main_layout.setMargin(4)
        main_layout.setSpacing(4)

        main_layout.addWidget(self.header)
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.progressBar)
        main_layout.addWidget(self.button)

    def create_connections(self):
        self.button.pressed.connect(self.initDownload)

    def initDownload(self):
        self.button.setText("Downloading file...")
        # Disable the button while the file is downloading.
        self.button.setEnabled(False)
        # Run the download in a new thread.
        self.downloader = Downloader(
            FFMPEG_URL,
            FFMPEG_FILENAME
        )
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

def run(*args):  # @unusedVariable

    tool = DownloadWindow()
    tool.show()

if __name__ == "__main__":
    run()