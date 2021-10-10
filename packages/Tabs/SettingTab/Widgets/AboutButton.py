from PySide2.QtCore import Signal
from PySide2.QtWidgets import QPushButton, QFileDialog

from packages.Startup import GlobalFiles
from packages.Tabs.SettingTab.Widgets.AboutDialog import AboutDialog


def open_about_dialog():
    about_dialog = AboutDialog()
    about_dialog.execute()


class AboutButton(QPushButton):
    clear_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setIcon(GlobalFiles.AboutIcon)
        self.setText(" About")
        self.hint_when_enabled = "About Us"
        self.setToolTip(self.hint_when_enabled)
        self.clicked.connect(open_about_dialog)
