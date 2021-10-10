from packages.Widgets.YesNoDialog import YesNoDialog


class ReloadAudioFilesDialog(YesNoDialog):
    def __init__(self):
        super().__init__()
        self.message.setText(
            "Are you sure ?\nThis will reload all audio files and will affect current matching")
        self.setWindowTitle("Change Audio Files")

    def execute(self):
        self.exec_()
