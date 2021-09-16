from packages.Startup import GlobalFiles
from packages.Widgets.YesNoDialog import YesNoDialog


class ClearAttachmentFilesDialog(YesNoDialog):
    def __init__(self):
        super().__init__()
        self.message.setText(
            "Are you sure ?\nThis will clear all attachment files")
        self.setWindowTitle("Clear Attachment Files")
        self.setWindowIcon(GlobalFiles.NoMarkIcon)

    def execute(self):
        self.exec_()
