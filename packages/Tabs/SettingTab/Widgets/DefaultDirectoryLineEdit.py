from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLineEdit


class DefaultDirectoryLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
