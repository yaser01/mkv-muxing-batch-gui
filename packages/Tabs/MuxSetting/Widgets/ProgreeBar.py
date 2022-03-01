from PySide2.QtWidgets import QProgressBar, QStyleFactory

from packages.Startup.GlobalFiles import WindowsStyle


class ProgressBar(QProgressBar):
    def __init__(self, value=0, show_percentage=False):
        super().__init__()
        self.value = value
        self.setValue(self.value)
        self.setTextVisible(show_percentage)
        self.setStyle(WindowsStyle)
