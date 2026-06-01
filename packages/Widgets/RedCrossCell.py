from PySide6.QtGui import QPixmap, Qt, QResizeEvent
from PySide6.QtWidgets import QLabel

from packages.Startup import GlobalFiles


class RedCrossCell(QLabel):
    def __init__(self, tool_tip):
        super().__init__()
        self._pixmap = QPixmap(GlobalFiles.RedCrossMarkIconPath)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setToolTip(tool_tip)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.setPixmap(
            self._pixmap.scaled(
                self.width(), self.height() - 5, Qt.AspectRatioMode.KeepAspectRatio
            )
        )