import webbrowser

from PySide2 import QtGui, QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QLabel, \
    QDialog, QPushButton, QHBoxLayout

from packages.Startup import GlobalFiles


def click_show_log_file():
    webbrowser.open(GlobalFiles.LogFilePath)


class OkDialog(QDialog):
    def __init__(self, window_title, parent=None):
        super().__init__(parent)
        self.info_message = ""
        self.window_title = window_title
        self.message = QLabel()
        self.mux_good_photo_label = QLabel()
        self.mux_good_photo_label.setPixmap(QtGui.QPixmap(GlobalFiles.GoodJobIconPath))
        self.messageIcon = QLabel()
        self.yes_button = QPushButton("OK")
        self.show_log_file_button = QPushButton("Open log file")

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.yes_button)
        self.buttons_layout.addWidget(self.show_log_file_button)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.mux_good_photo_label, 0, 0, 3, 4, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.buttons_layout, 3, 1, 1, 2)
        self.main_layout.setContentsMargins(10, 20, 10, 20)
        self.setLayout(self.main_layout)

        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()
        self.set_message_icon_ok()
        self.set_dialog_values()
        # self.increase_message_font_size(1)
        self.set_default_buttons()

    def set_message_icon_ok(self):
        self.messageIcon.setPixmap(QtGui.QPixmap(GlobalFiles.OkIconPath))

    def signal_connect(self):
        self.yes_button.clicked.connect(self.click_yes)
        self.show_log_file_button.clicked.connect(click_show_log_file)

    def click_yes(self):
        self.close()

    def set_dialog_values(self):
        self.setWindowTitle(self.window_title)
        self.setWindowIcon(GlobalFiles.OkIcon)
        self.message.setText(self.info_message)

    def disable_question_mark_window(self):
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, on=False)

    def increase_message_font_size(self, value):
        message_font = self.message.font()
        message_font.setPointSize(self.message.fontInfo().pointSize() + value)
        self.message.setFont(message_font)

    def set_default_buttons(self):
        self.yes_button.setDefault(True)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.size())

    def execute(self):
        self.exec_()
