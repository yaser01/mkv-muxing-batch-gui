import PySide2
from PySide2.QtGui import QPixmap, Qt
from PySide2.QtWidgets import QLabel

from packages.Startup import GlobalFiles


class RedCrossCell(QLabel):
    def __init__(self, tool_tip):
        super().__init__()
        self.pixmap = QPixmap(GlobalFiles.RedCrossMarkIconPath)
        self.setAlignment(Qt.AlignCenter)
        self.setToolTip(tool_tip)

    def resizeEvent(self, event: PySide2.QtGui.QResizeEvent):
        super().resizeEvent(event)
        self.setPixmap(self.pixmap.scaled(self.width(), self.height() - 5, Qt.KeepAspectRatio))
