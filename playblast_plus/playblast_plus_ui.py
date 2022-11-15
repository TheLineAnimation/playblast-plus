import sys

from maya import OpenMayaUI as omui
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance 

from lib.mayaLogger import MayaLogger

def get_maya_main_window():
    """Returns the Maya main window widget as a Python object.
    Updated to handle Python 3 int/long casting
    Returns:
      A Qwidget instance of the the Maya main window
    """
    main_window_ptr = omui.MQtUtil.mainWindow()

    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class PlayBlastPlusLogger(MayaLogger):
    """
    Set up a custom script logger
    """
    LOGGER_NAME = "PlayBlastPlusLogger"
    