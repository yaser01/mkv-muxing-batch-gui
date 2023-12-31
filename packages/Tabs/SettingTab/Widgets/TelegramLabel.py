import webbrowser

from PySide2.QtCore import Qt
from PySide2.QtGui import QMouseEvent, QPixmap, QCursor
from PySide2.QtWidgets import QLabel

from packages.Startup.GlobalFiles import TelegramIconPath


class TelegramLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setPixmap(QPixmap(TelegramIconPath))
        self.setToolTip("https://t.me/yaser01")
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        webbrowser.open('https://t.me/yaser01')
