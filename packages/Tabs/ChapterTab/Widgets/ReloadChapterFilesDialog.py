from packages.Widgets.ReloadFilesDialog import ReloadFilesDialog


class ReloadChapterFilesDialog(ReloadFilesDialog):
    def __init__(self):
        super().__init__()
        self.message.setText(
            "Are you sure ?\nThis will reload all chapter files and will affect current matching")
        self.setWindowTitle("Change Chapter Files")

    def execute(self):
        self.exec_()
