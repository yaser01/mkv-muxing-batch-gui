import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent, QPixmap, QCursor
from PySide6.QtWidgets import QLabel

from packages.Startup.GlobalFiles import TwitterIconPath


class TwitterLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setPixmap(QPixmap(TwitterIconPath))
        self.setToolTip("https://twitter.com/yasserm001")
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        webbrowser.open('https://twitter.com/yasserm001')
