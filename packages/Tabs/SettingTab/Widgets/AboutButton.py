from PySide6.QtWidgets import QPushButton

from packages.Startup import GlobalIcons
from packages.Tabs.SettingTab.Widgets.AboutDialog import AboutDialog


class AboutButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(GlobalIcons.AboutIcon)
        self.setText(" About")
        self.hint_when_enabled = "About Us"
        self.setToolTip(self.hint_when_enabled)
        self.clicked.connect(self.open_about_dialog)

    def open_about_dialog(self):
        about_dialog = AboutDialog(parent=self)
        about_dialog.execute()
