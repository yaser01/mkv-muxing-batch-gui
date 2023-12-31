from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QGridLayout, QLabel, \
     QPushButton, QHBoxLayout

from packages.Startup import GlobalFiles
from packages.Startup import GlobalIcons
from packages.Widgets.MyDialog import MyDialog


class NoSettingToApplyDialog(MyDialog):
    """
    NoSettingToApplyDialog class to create an dialog with confirmation button
    You can check for result after calling `NoSettingToApplyDialog.execute()`
    By checking of value `NoSettingToApplyDialog.result` which can be either [Cancel/Muxing]
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.info_message = "You haven't select any setting to apply"
        self.window_title = "No Setting Selected"
        self.result = "Cancel"
        self.message = QLabel()
        self.messageIcon = QLabel()
        self.yes_button = QPushButton("Confirm Muxing")
        self.no_button = QPushButton("Cancel")
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.yes_button)
        self.buttons_layout.addWidget(self.no_button)
        self.main_layout_spacer_item = QLabel()
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.messageIcon, 0, 0, 2, 1)
        self.main_layout.addWidget(self.main_layout_spacer_item, 0, 1, 1, 1)  # add space
        self.main_layout.addWidget(self.message, 0, 2, 2, 3)
        self.main_layout.addLayout(self.buttons_layout, 2, 4, 1, -1)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)

        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()
        self.set_dialog_values()
        self.set_message_icon_info()
        # self.increase_message_font_size(1)
        self.set_default_buttons()

    def set_message_icon_info(self):
        self.messageIcon.setPixmap(QtGui.QPixmap(GlobalFiles.InfoBigIconPath))

    def signal_connect(self):
        self.yes_button.clicked.connect(self.click_yes)
        self.no_button.clicked.connect(self.click_no)

    def click_yes(self):
        self.result = "Muxing"
        self.close()

    def click_no(self):
        self.result = "Cancel"
        self.close()

    def set_dialog_values(self):
        self.setWindowTitle(self.window_title)
        self.message.setText(self.info_message)
        self.setWindowIcon(GlobalIcons.InfoIcon)

    def disable_question_mark_window(self):
        self.setWindowFlag(QtCore.Qt.WindowType.WindowContextHelpButtonHint, on=False)

    def increase_message_font_size(self, value):
        message_font = self.message.font()
        message_font.setPointSize(self.message.fontInfo().pointSize() + value)
        self.message.setFont(message_font)

    def set_default_buttons(self):
        self.no_button.setDefault(True)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.size())

    def execute(self):
        self.exec()
