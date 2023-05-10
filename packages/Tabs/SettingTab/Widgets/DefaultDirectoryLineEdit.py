from PySide2.QtWidgets import QLineEdit


class DefaultDirectoryLineEdit(QLineEdit):
    def __init__(self, default_directory):
        super().__init__()
        self.setReadOnly(True)
        self.setText(default_directory)
