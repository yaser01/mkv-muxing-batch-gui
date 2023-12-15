from packages.Widgets.YesNoDialog import YesNoDialog


class ReloadVideoFilesDialog(YesNoDialog):
    def __init__(self):
        super().__init__()
        self.message.setText(
            "Are you sure ?\nThis will reload all video files and will affect Matching in other tabs")
        self.setWindowTitle("Change Video Files")

    def execute(self):
        self.exec()
