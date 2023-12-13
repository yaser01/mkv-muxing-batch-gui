from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QSizePolicy, QLabel
)

from packages.Startup import GlobalFiles


class InfoWithOptionsCell(QLabel):
    def __init__(self, tool_tip="", parent=None):
        super().__init__(parent)
        self.setPixmap(QtGui.QPixmap(GlobalFiles.InfoSettingIconPath))
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_tool_tip(tool_tip)
        self.setToolTipDuration(10000)

    def update_tool_tip(self, tool_tip):
        self.setToolTip(tool_tip)
