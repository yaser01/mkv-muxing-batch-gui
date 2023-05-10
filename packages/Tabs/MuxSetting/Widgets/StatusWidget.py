from PySide2.QtCore import QSize
from PySide2.QtGui import QMovie
from PySide2.QtWidgets import QWidget, QHBoxLayout, QLabel

from packages.Startup.GlobalFiles import SpinnerIconPath


class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.status_label = QLabel("  0%")
        self.load_icon_movie = QMovie(SpinnerIconPath)
        self.load_icon_movie.setScaledSize(QSize(26, 26))
        self.load_icon_label = QLabel()
        self.load_icon_label.setMovie(self.load_icon_movie)

        self.layout = QHBoxLayout()
        self.layout.addStretch(2)
        self.layout.addWidget(self.load_icon_label)
        self.layout.addWidget(self.status_label)
        self.layout.addStretch(3)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def update_progress(self, new_progress):
        self.status_label.setText("  "+str(new_progress) + "%")

    def start_loading(self):
        self.load_icon_movie.start()

    def stop_loading(self):
        self.load_icon_movie.stop()
