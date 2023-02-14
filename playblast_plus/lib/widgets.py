from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import os

from . import settings

class ToolHeader(QtWidgets.QWidget):
    """A standardised Tool Header widget, with line Logo and a settable script name field.

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
    # STYLE_SHEET = 'font-weight: bold; color: rgb(205, 205, 205);background-color: rgb(30,30,30);'

    STYLE_SHEET = ("font: bold 14px;"
                 "color: rgb(205, 205, 205);"
                 "height: 25px;"
                 "background-color: rgb(30,30,30);"
                 "border:1px solid black;"
                 "border-radius:4px;"
                 )

    def __init__(self, name='', text= '', parent=None):
            super(ToolHeader, self).__init__(parent)
            self.name = name
            self.headerTitle = text
            self.registerUserData = ""            
            self.setMinimumSize(QtCore.QSize(160, 46))
            self.setStyleSheet(self.STYLE_SHEET)             
            self.create_widgets()
            self.create_layout()
            self.create_actions()

    def create_widgets(self):
            
        self.labelIcon = QtWidgets.QLabel()
        self.labelIcon.setStyleSheet(self.STYLE_SHEET)          
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, 
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.labelIcon.sizePolicy().hasHeightForWidth())
        self.labelIcon.setMaximumSize(QtCore.QSize(160, 40))
        self.labelIcon.setSizePolicy(sizePolicy) 
        self.labelText = QtWidgets.QLabel()
        self.labelText.setStyleSheet(self.STYLE_SHEET)
        self.labelText.setText(self.headerTitle)
        self.labelText.setMaximumSize(QtCore.QSize(16777215, 40)) 
        self.labelText.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.labelText.setIndent(4)

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
    
    def create_actions(self):
        pass
            
    def addHeaderIcon(self, widget):
        icon_root = settings.get_resources_directory()
            
        if icon_root:
            image_path = os.path.join (icon_root,self.LINE_LOGO)
            image = QtGui.QImage(image_path)
            pixmap = QtGui.QPixmap()
            pixmap.convertFromImage(image)
            widget.setPixmap(pixmap)

    def iconClicked(self):
        pass
        