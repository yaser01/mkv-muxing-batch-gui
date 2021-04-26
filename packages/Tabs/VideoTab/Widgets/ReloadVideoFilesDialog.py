from packages.Widgets.ReloadFilesDialog import ReloadFilesDialog


class ReloadVideoFilesDialog(ReloadFilesDialog):
    def __init__(self):
        super().__init__()
        self.message.setText(
            "Are you sure ?\nThis will reload all video files and will affect Matching in other tabs")
        self.setWindowTitle("Change Video Files")

    def execute(self):
        self.exec_()
