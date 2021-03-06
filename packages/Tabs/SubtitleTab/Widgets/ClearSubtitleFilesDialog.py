from packages.Startup import GlobalFiles
from packages.Widgets.YesNoDialog import YesNoDialog


class ClearSubtitleFilesDialog(YesNoDialog):
    def __init__(self):
        super().__init__()
        self.message.setText(
            "Are you sure ?\nThis will clear all subtitle files")
        self.setWindowTitle("Clear Subtitle Files")
        self.setWindowIcon(GlobalFiles.NoMarkIcon)

    def execute(self):
        self.exec_()
