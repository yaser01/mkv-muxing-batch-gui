from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QLabel, \
    QDialog, QPushButton, QHBoxLayout

from packages.Startup import GlobalFiles


class InvalidPathDialog(QDialog):
    def __init__(self, window_title="Invalid Path", error_message="Please Enter a Valid Path", parent=None):
        super().__init__(parent)
        self.error_message = error_message
        self.window_title = window_title
        self.message = QLabel()
        self.messageIcon = QLabel()
        self.yesButton = QPushButton("OK")

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.yesButton)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.messageIcon, 0, 0, 2, 1)
        self.main_layout.addWidget(QLabel(), 0, 1, 1, 1)  # add space
        self.main_layout.addWidget(self.message, 0, 2, 2, 3)
        self.main_layout.addLayout(self.buttons_layout, 2, 4, 1, 1)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)

        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()
        self.set_message_icon_critical()
        self.set_dialog_values()
        # self.increase_message_font_size(1)
        self.set_default_buttons()

    def signal_connect(self):
        self.yesButton.clicked.connect(self.click_yes)

    def click_yes(self):
        self.close()

    def set_dialog_values(self):
        self.setWindowTitle(self.window_title)
        self.message.setText(self.error_message)
        self.setWindowIcon(GlobalFiles.ErrorIcon)

    def disable_question_mark_window(self):
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)

    def increase_message_font_size(self, value):
        message_font = self.message.font()
        message_font.setPointSize(self.message.fontInfo().pointSize() + value)
        self.message.setFont(message_font)

    def set_message_icon_critical(self):
        self.messageIcon.setPixmap(QtGui.QPixmap(GlobalFiles.ErrorBigIconPath))

    def set_default_buttons(self):
        self.yesButton.setDefault(True)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.size())

    def execute(self):
        self.exec_()
