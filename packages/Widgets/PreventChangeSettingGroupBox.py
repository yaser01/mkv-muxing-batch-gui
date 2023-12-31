from PySide2.QtWidgets import QHBoxLayout, QGroupBox, QLabel

from packages.Startup import GlobalFiles


class PreventChangeSettingGroupBox(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle("")
        self.setStyleSheet("QGroupBox {border:none}")
        self.setFlat(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.prevent_change_setting_layout = QHBoxLayout()
        self.prevent_change_setting_icon = QLabel()
        self.prevent_change_setting_text = QLabel()
        self.prevent_change_setting_icon.setPixmap(GlobalFiles.InfoIconPath)
        self.prevent_change_setting_text.setText("change setting disabled")
        self.prevent_change_setting_text.setContentsMargins(0, 0, 0, 1)
        self.prevent_change_setting_layout.setContentsMargins(0, 0, 0, 5)
        self.prevent_change_setting_layout.addWidget(self.prevent_change_setting_icon)
        self.prevent_change_setting_layout.addWidget(self.prevent_change_setting_text)
        self.setToolTip("You can't change global settings while job queue has unfinished job(s)")
        self.setToolTipDuration(12000)
        self.setLayout(
            self.prevent_change_setting_layout)
