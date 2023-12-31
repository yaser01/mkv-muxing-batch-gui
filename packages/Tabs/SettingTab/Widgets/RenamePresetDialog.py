from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QHBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit

from packages.Startup import GlobalIcons
from packages.Widgets.MyDialog import MyDialog


class RenamePresetDialog(MyDialog):
    def __init__(self, parent=None, old_name="Preset"):
        super().__init__(parent)
        self.setWindowTitle("Rename Preset")
        self.setWindowIcon(GlobalIcons.RenameIcon)
        self.message = QLabel()
        self.message.setText("Rename Preset To: ")
        self.yes_button = QPushButton("OK")
        self.no_button = QPushButton("Cancel")
        self.new_name = old_name
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.no_button)
        self.buttonLayout.addWidget(self.yes_button)

        self.line_edit = QLineEdit()
        self.line_edit.setText(old_name)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.message, 0, 0)
        self.main_layout.addWidget(self.line_edit, 0, 1)
        self.main_layout.addLayout(self.buttonLayout, 1, 0, -1, -1)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.result = "No"
        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()
        self.set_default_buttons()

    def signal_connect(self):
        self.yes_button.clicked.connect(self.click_yes)
        self.no_button.clicked.connect(self.click_no)
        pass

    def click_yes(self):
        self.result = "Yes"
        self.new_name = self.line_edit.text()
        self.close()

    def click_no(self):
        self.result = "No"
        self.close()

    def disable_question_mark_window(self):
        self.setWindowFlag(QtCore.Qt.WindowType.WindowContextHelpButtonHint, on=False)

    def increase_message_font_size(self, value):
        message_font = self.message.font()
        message_font.setPointSize(self.message.fontInfo().pointSize() + value)
        self.message.setFont(message_font)

    def reset_dialog_values(self):
        self.setWindowTitle("")  # determine when use
        self.message.setText("")  # determine when use

    def set_default_buttons(self):
        self.yes_button.setDefault(True)
        self.no_button.setDefault(False)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.size())

    def execute(self):
        self.exec()
