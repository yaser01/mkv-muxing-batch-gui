from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QGridLayout, QLabel, \
    QDialog, QPushButton, QHBoxLayout

from packages.Startup import GlobalFiles


class CloseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.info_message = "Are you sure you want to exit ?\nThis will stop current muxing"
        self.window_title = "Confirm Exit"
        self.message = QLabel()
        self.messageIcon = QLabel()
        self.exit_button = QPushButton("Stop Muxing")
        self.cancel_button = QPushButton("Cancel")
        self.result = "Cancel"
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.exit_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.messageIcon, 0, 0, 2, 1)
        self.main_layout.addWidget(QLabel(), 0, 1, 1, 1)  # add space
        self.main_layout.addWidget(self.message, 0, 2, 2, 3)
        self.main_layout.addLayout(self.buttons_layout, 2, 0, -1, -1)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)

        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()
        self.set_message_icon_warning()
        self.set_dialog_values()
        # self.increase_message_font_size(1)
        self.set_default_buttons()

    def set_message_icon_warning(self):
        self.messageIcon.setPixmap(QtGui.QPixmap(GlobalFiles.WarningCheckBigIconPath))

    def signal_connect(self):
        self.exit_button.clicked.connect(self.click_exit)
        self.cancel_button.clicked.connect(self.click_cancel)

    def click_cancel(self):
        self.result = "Cancel"
        self.close()

    def click_exit(self):
        self.result = "Exit"
        self.close()

    def set_dialog_values(self):
        self.setWindowTitle(self.window_title)
        self.setWindowIcon(GlobalFiles.WarningCheckBigIcon)
        self.message.setText(self.info_message)

    def disable_question_mark_window(self):
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, on=False)

    def increase_message_font_size(self, value):
        message_font = self.message.font()
        message_font.setPointSize(self.message.fontInfo().pointSize() + value)
        self.message.setFont(message_font)

    def set_default_buttons(self):
        self.cancel_button.setDefault(True)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.size())

    def execute(self):
        self.exec_()
