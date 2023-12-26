from packages.Startup import GlobalIcons
from packages.Widgets.YesNoDialog import YesNoDialog


class ClearAudioFilesDialog(YesNoDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.message.setText(
            "Are you sure ?\nThis will clear all audio files")
        self.setWindowTitle("Clear Audio Files")
        self.setWindowIcon(GlobalIcons.NoMarkIcon)

    def execute(self):
        self.exec()
