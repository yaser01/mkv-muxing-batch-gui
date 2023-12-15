from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout

from packages.Startup.InitializeScreenResolution import screen_size
from packages.Tabs.VideoTab.Widgets.MediaInfoTreeWidget import MediaInfoTreeWidget
from packages.Widgets.MyDialog import MyDialog


class VideoInfoDialog(MyDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Info")
        self.main_layout = QVBoxLayout()
        self.tree = MediaInfoTreeWidget()
        self.expand_all_button = QPushButton("Expand All")
        self.collapse_all_button = QPushButton("Collapse All")
        self.button_layout = QHBoxLayout()
        self.setup_button_layout()
        self.setup_main_layout()
        self.setup_window_dimension()
        self.disable_question_mark_window()
        self.setLayout(self.main_layout)
        self.connect_signals()

    def setup_window_dimension(self):
        self.setMinimumWidth(screen_size.width() // 2)
        self.setMinimumHeight(screen_size.height() // 2)
        self.setContentsMargins(screen_size.width() // 500, screen_size.width() // 500, screen_size.width() // 500,
                                screen_size.width() // 500)

    def setup_main_layout(self):
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.tree)

    def setup_button_layout(self):
        self.button_layout.addStretch(5)
        self.button_layout.addWidget(self.expand_all_button, alignment=Qt.AlignmentFlag.AlignRight, stretch=0)
        self.button_layout.addWidget(self.collapse_all_button, alignment=Qt.AlignmentFlag.AlignRight, stretch=0)

    def disable_question_mark_window(self):
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, on=False)

    def connect_signals(self):
        self.expand_all_button.clicked.connect(self.expand_tree)
        self.collapse_all_button.clicked.connect(self.collapse_tree)

    def expand_tree(self):
        self.tree.expandAll()

    def collapse_tree(self):
        self.tree.collapseAll()

    def execute(self):
        self.exec()
