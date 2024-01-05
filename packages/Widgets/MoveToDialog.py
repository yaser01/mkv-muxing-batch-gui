from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QHBoxLayout, \
     QSpinBox, QGridLayout, QLabel, QPushButton, QAbstractSpinBox

from packages.Widgets.MyDialog import MyDialog


class MoveToDialog(MyDialog):
    def __init__(self, parent=None, min=1, max=1):
        super().__init__(parent)
        self.message = QLabel()
        self.extra_message = QLabel()
        self.yesButton = QPushButton("OK")
        self.noButton = QPushButton("Cancel")

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.noButton)
        self.buttonLayout.addWidget(self.yesButton)

        self.spinBox = QSpinBox()
        self.spinBox.setMinimum(min)
        self.spinBox.setMaximum(max)
        self.spinBox.stepBy(1)
        self.spinBox.setFocus()

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.message, 0, 0)
        self.main_layout.addWidget(self.spinBox, 0, 1)
        self.main_layout.addWidget(self.extra_message, 1, 0, 1, 2)
        self.main_layout.addLayout(self.buttonLayout, 2, 0, -1, -1)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.result = "No"
        self.position = -1
        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()
        self.reset_dialog_values()
        self.disable_spinbox_buttons()
        # self.increase_message_font_size(1)
        self.set_default_buttons()

    def signal_connect(self):
        self.yesButton.clicked.connect(self.click_yes)
        self.noButton.clicked.connect(self.click_no)
        pass

    def click_yes(self):
        self.result = "Yes"
        self.position = self.spinBox.value()
        self.close()

    def click_no(self):
        self.result = "No"
        self.position = -1
        self.close()

    def disable_question_mark_window(self):
        self.setWindowFlag(QtCore.Qt.WindowType.WindowContextHelpButtonHint, on=False)

    def increase_message_font_size(self, value):
        message_font = self.message.font()
        message_font.setPointSize(self.message.fontInfo().pointSize() + value)
        self.message.setFont(message_font)
        self.extra_message.setFont(message_font)

    def reset_dialog_values(self):
        self.setWindowTitle("")  # determine when use
        self.message.setText("")  # determine when use
        self.extra_message.setText("")  # determine when use

    def disable_spinbox_buttons(self):
        self.spinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

    def set_default_buttons(self):
        self.yesButton.setDefault(True)
        self.noButton.setDefault(False)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.spinBox.selectAll()
        self.setFixedSize(self.size())

    def execute(self):
        self.exec()
