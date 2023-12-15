from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QGridLayout, QLabel, \
     QPushButton, QHBoxLayout, QFormLayout

from packages.Startup import GlobalFiles
from packages.Startup import GlobalIcons
from packages.Widgets.MyDialog import MyDialog


class ChapterInfoDialog(MyDialog):
    def __init__(self, chapter_name="Test", parent=None):
        super().__init__(parent)
        self.window_title = "Chapter Info"
        self.messageIcon = QLabel()
        self.chapter_name_label = QLabel("Chapter Name:")
        self.chapter_name_value = QLabel(str(chapter_name))

        self.yes_button = QPushButton("OK")

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addStretch(stretch=4)
        self.buttons_layout.addWidget(self.yes_button, stretch=3)
        self.buttons_layout.addStretch(stretch=4)
        self.chapter_setting_layout = QGridLayout()
        self.chapter_editable_setting_layout = QFormLayout()
        self.chapter_editable_setting_layout.addRow(self.chapter_name_label, self.chapter_name_value)
        self.chapter_setting_layout.addLayout(self.chapter_editable_setting_layout, 1, 0, 4, 2)
        self.chapter_setting_layout.addWidget(self.messageIcon, 0, 3, 5, -1)

        self.main_layout = QGridLayout()
        self.main_layout.addLayout(self.chapter_setting_layout, 0, 0, 2, 3)
        self.main_layout.addLayout(self.buttons_layout, 2, 0, 1, -1)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)

        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()
        self.messageIcon.setPixmap(QtGui.QPixmap(GlobalFiles.ChapterIconPath).scaledToHeight(60))
        self.set_dialog_values()
        # self.increase_message_font_size(1)
        self.set_default_buttons()

    def signal_connect(self):
        self.yes_button.clicked.connect(self.click_yes)

    def click_yes(self):
        self.close()

    def set_dialog_values(self):
        self.setWindowTitle(self.window_title)
        self.setWindowIcon(GlobalIcons.InfoIcon)

    def disable_question_mark_window(self):
        self.setWindowFlag(QtCore.Qt.WindowType.WindowContextHelpButtonHint, on=False)

    def set_default_buttons(self):
        self.yes_button.setDefault(True)
        self.yes_button.setFocus()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.size())

    def execute(self):
        self.exec_()
