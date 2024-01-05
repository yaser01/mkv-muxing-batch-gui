from sys import platform

from PySide6.QtWidgets import QProgressBar, QStyleFactory

from packages.Startup.SetupThems import get_dark_palette


class ProgressBar(QProgressBar):
    def __init__(self, value=0, show_percentage=False):
        super().__init__()
        self.value = value
        self.setValue(self.value)
        self.setTextVisible(show_percentage)
        return
        if platform == "win32":
            self.setStyle(QStyleFactory.create("windowsvista"))
            self.setPalette(get_dark_palette())
