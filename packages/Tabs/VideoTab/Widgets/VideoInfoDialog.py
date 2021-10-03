from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPalette, qRgba
from PySide2.QtWidgets import QDialog, QTreeWidgetItem, QHBoxLayout, QTreeWidget

from packages.Startup.InitializeScreenResolution import screen_size
from packages.Tabs.VideoTab.Widgets.MediaInfoTreeWidget import MediaInfoTreeWidget
from packages.Widgets.TreeWidget import TreeWidget


class VideoInfoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Info")
        self.main_layout = QHBoxLayout()
        self.tree = MediaInfoTreeWidget()
        self.main_layout.addWidget(self.tree)
        self.setLayout(self.main_layout)
        self.setMinimumWidth(screen_size.width() // 2)
        self.setMinimumHeight(screen_size.height() // 2)
        self.disable_question_mark_window()

    def disable_question_mark_window(self):
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)

    def execute(self):
        self.exec_()
