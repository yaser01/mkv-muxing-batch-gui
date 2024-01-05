from packages.Widgets.YesNoDialog import YesNoDialog


class ReloadAudioFilesDialog(YesNoDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.message.setText(
            "Are you sure ?\nThis will reload all audio files and will affect current matching")
        self.setWindowTitle("Change Audio Files")

    def execute(self):
        self.exec()
