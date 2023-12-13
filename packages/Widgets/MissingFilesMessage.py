from PySide6.QtWidgets import QMessageBox


class MissingFilesMessage(QMessageBox):
    def __init__(self, error_message):
        super().__init__()
        self.setIcon(QMessageBox.Icon.Critical)
        self.setText("Missing Files")
        self.setInformativeText(error_message)
        self.setWindowTitle("Error")

    def execute(self):
        self.exec_()
