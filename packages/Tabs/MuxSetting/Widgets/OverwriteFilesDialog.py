from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton, QGridLayout, QHBoxLayout

from packages.Startup import GlobalFiles, GlobalIcons
from packages.Widgets.MyDialog import MyDialog


class OverwriteFilesDialog(MyDialog):
    """
    OverwriteFilesDialog class to create a dialog with confirmation button
    You can check for result after calling `OverwriteFilesDialog.execute()`
    By checking of value `OverwriteFilesDialog.result` which can be either [Overwrite/Cancel]
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.info_message = "<nobr>You are going to overwrite your source files this <b>can't be undone</b><br>There is no back, you will lost your source files"
        self.window_title = "Empty Destination Path"
        self.message = QLabel()
        self.messageIcon = QLabel()
        self.yes_button = QPushButton("Overwrite Files")
        self.no_button = QPushButton("Cancel")
        self.result = "Cancel"
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(QLabel(""))
        self.buttons_layout.addWidget(self.yes_button)
        self.buttons_layout.addWidget(self.no_button)
        self.buttons_layout.addWidget(QLabel(""))

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.messageIcon, 0, 0, 2, 1)
        self.main_layout.addWidget(QLabel(), 0, 1, 1, 1)  # add space
        self.main_layout.addWidget(self.message, 0, 2, 2, 3)
        self.main_layout.addLayout(self.buttons_layout, 2, 2, 1, -1)
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
        self.yes_button.clicked.connect(self.click_yes)
        self.no_button.clicked.connect(self.click_no)

    def click_yes(self):
        self.result = "Overwrite"
        self.close()

    def click_no(self):
        self.result = "Cancel"
        self.close()

    def set_dialog_values(self):
        self.setWindowTitle(self.window_title)
        self.setWindowIcon(GlobalIcons.WarningCheckIcon)
        self.message.setText(self.info_message)

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
        self.exec_()

    def execute_wth_no_block(self):
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.show()
