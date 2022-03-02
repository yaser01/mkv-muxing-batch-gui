import time

from PySide2.QtCore import QSize
from PySide2.QtWidgets import QPushButton

from packages.Startup.GlobalFiles import SettingIcon
from packages.Tabs.SettingTab.SettingDialog import SettingDialog


class SettingButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(SettingIcon)
        self.setIconSize(QSize(18, 18))
        self.setText(" Options")
        self.clicked.connect(self.open_setting_dialog)

    def open_setting_dialog(self):
        for i in range(2000):
            try:
                setting_dialog = SettingDialog()
                setting_dialog.execute()
                break
            except Exception as e:
                time.sleep(0.003)
