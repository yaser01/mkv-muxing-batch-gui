from PySide2 import QtGui, QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QHBoxLayout, \
    QDialog, QSpinBox, QGridLayout, QLabel, QPushButton, QAbstractSpinBox

from packages.Startup.GlobalFiles import SettingIcon
from packages.Startup.InitializeScreenResolution import screen_size, height_factor
from packages.Tabs.SettingTab.SettingTabWidget import SettingTabWidget


class SettingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(SettingIcon)
        self.setWindowTitle("Options")
        self.setMinimumWidth(screen_size.width() // 1.7)
        self.setMinimumHeight(int(height_factor * 635 * 0.71))
        self.setMaximumHeight(int(height_factor * 635 * 0.71))
        self.message = QLabel()
        self.extra_message = QLabel()
        self.yes_button = QPushButton("OK")
        self.no_button = QPushButton("Cancel")

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(QLabel(""), stretch=3)
        self.buttons_layout.addWidget(self.no_button, stretch=2)
        self.buttons_layout.addWidget(self.yes_button, stretch=2)
        self.buttons_layout.addWidget(QLabel(""), stretch=3)
        self.setting_tab_widget = SettingTabWidget()

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.setting_tab_widget, 0, 0, 1, 1)
        self.main_layout.addLayout(self.buttons_layout, 1, 0, 1, 1)
        self.main_layout.setRowStretch(1, 0)
        self.main_layout.setRowStretch(0, 0)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.result = "No"
        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()

    def signal_connect(self):
        self.yes_button.clicked.connect(self.click_yes)
        self.no_button.clicked.connect(self.click_no)
        pass

    def click_yes(self):
        self.result = "Yes"
        self.close()

    def click_no(self):
        self.result = "No"
        self.close()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)

    def disable_question_mark_window(self):
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)

    def execute(self):
        self.exec_()
