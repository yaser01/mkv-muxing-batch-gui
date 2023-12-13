from PySide6.QtWidgets import QPushButton

from packages.Startup import GlobalIcons
from packages.Tabs.SettingTab.Widgets.AboutDialog import AboutDialog


def open_about_dialog():
    about_dialog = AboutDialog()
    about_dialog.execute()


class AboutButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(GlobalIcons.AboutIcon)
        self.setText(" About")
        self.hint_when_enabled = "About Us"
        self.setToolTip(self.hint_when_enabled)
        self.clicked.connect(open_about_dialog)
