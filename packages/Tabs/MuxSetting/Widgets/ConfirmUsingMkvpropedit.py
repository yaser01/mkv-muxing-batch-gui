from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QGridLayout, QLabel, \
     QApplication, QStyle, QPushButton, QHBoxLayout

from packages.Widgets.MyDialog import MyDialog


def get_pixmap_from_info_icon():
    style = QApplication.style()
    size = style.pixelMetric(QStyle.PixelMetric.PM_MessageBoxIconSize, None, None)
    icon = style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation, None, None)
    return icon.pixmap(size, size)


def get_pixmap_from_warning_icon():
    style = QApplication.style()
    size = style.pixelMetric(QStyle.PixelMetric.PM_MessageBoxIconSize, None, None)
    icon = style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning, None, None)
    return icon.pixmap(size, size)


def get_pixmap_from_critical_icon():
    style = QApplication.style()
    size = style.pixelMetric(QStyle.PixelMetric.PM_MessageBoxIconSize, None, None)
    icon = style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical, None, None)
    return icon.pixmap(size, size)


class ConfirmUsingMkvpropedit(MyDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fast_muxing_button = QPushButton("Fast Muxing")
        self.cancel_button = QPushButton("Cancel")
        self.usual_muxing_button = QPushButton("Usual Muxing")
        self.setWindowTitle("We can make it faster")
        self.message = QLabel("<nobr>We can fast your muxing by editing the source files directly <br>This will "
                              "<b>overwrite</b> your video files and can't be undone")
        self.messageIcon = QLabel()

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.usual_muxing_button)
        self.buttons_layout.addWidget(self.fast_muxing_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.main_layout_spacer_item = QLabel()
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.messageIcon, 0, 0, 2, 1)
        self.main_layout.addWidget(self.main_layout_spacer_item, 0, 1, 1, 1)  # add space
        self.main_layout.addWidget(self.message, 0, 2, 2, 3)
        self.main_layout.addLayout(self.buttons_layout, 2, 4, 1, 1)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)

        self.result = "cancel"
        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()
        self.set_message_icon_info()
        # self.increase_message_font_size(1)
        self.set_default_buttons()

    def signal_connect(self):
        self.fast_muxing_button.clicked.connect(self.click_fast_muxing_button)
        self.cancel_button.clicked.connect(self.click_cancel_button)
        self.usual_muxing_button.clicked.connect(self.click_usual_muxing_button)

    def click_fast_muxing_button(self):
        self.result = "mkvpropedit"
        self.close()

    def click_cancel_button(self):
        self.result = "cancel"
        self.close()

    def click_usual_muxing_button(self):
        self.result = "mkvmerge"
        self.close()

    def reset_dialog_values(self):
        self.setWindowTitle("")  # determine when use
        self.message.setText("")  # determine when use

    def disable_question_mark_window(self):
        self.setWindowFlag(QtCore.Qt.WindowType.WindowContextHelpButtonHint, on=False)

    def increase_message_font_size(self, value):
        message_font = self.message.font()
        message_font.setPointSize(self.message.fontInfo().pointSize() + value)
        self.message.setFont(message_font)

    def set_message_icon_warning(self):
        self.messageIcon.setPixmap(get_pixmap_from_warning_icon())

    def set_message_icon_critical(self):
        self.messageIcon.setPixmap(get_pixmap_from_warning_icon())

    def set_message_icon_info(self):
        self.messageIcon.setPixmap(get_pixmap_from_info_icon())

    def set_default_buttons(self):
        self.fast_muxing_button.setDefault(False)
        self.cancel_button.setDefault(True)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.size())

    def execute(self):
        self.exec()
