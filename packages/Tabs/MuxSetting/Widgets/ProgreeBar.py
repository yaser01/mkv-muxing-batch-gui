from os import symlink
from PySide2.QtWidgets import QProgressBar, QStyleFactory
from sys import platform


class ProgressBar(QProgressBar):
    def __init__(self, value=0, show_percentage=False):
        super().__init__()
        self.value = value
        self.setValue(self.value)
        self.setTextVisible(show_percentage)
        if platform == "win32":
            self.setStyle(QStyleFactory.create("windowsvista"))
