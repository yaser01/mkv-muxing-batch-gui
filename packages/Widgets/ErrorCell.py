from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QSizePolicy, QLabel,
)

from packages.Startup import GlobalFiles


class ErrorCell(QLabel):
    def __init__(self, tool_tip="", parent=None):
        super().__init__(parent)
        self.setPixmap(QtGui.QPixmap(GlobalFiles.ErrorIconPath))
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setAlignment(Qt.AlignCenter)
        self.setToolTip(tool_tip)
        self.setToolTipDuration(10000)
