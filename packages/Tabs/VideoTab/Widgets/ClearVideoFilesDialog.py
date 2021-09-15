from packages.Startup import GlobalFiles
from packages.Widgets.YesNoDialog import YesNoDialog


class ClearVideoFilesDialog(YesNoDialog):
    def __init__(self):
        super().__init__()
        self.message.setText(
            "Are you sure ?\nThis will clear all video files")
        self.setWindowTitle("Clear Video Files")
        self.setWindowIcon(GlobalFiles.NoMarkIcon)

    def execute(self):
        self.exec_()
