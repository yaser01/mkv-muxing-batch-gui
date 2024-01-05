from packages.Widgets.YesNoDialog import YesNoDialog


class ReloadSubtitleFilesDialog(YesNoDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.message.setText(
            "Are you sure ?\nThis will reload all subtitle files and will affect current matching")
        self.setWindowTitle("Change Subtitle Files")

    def execute(self):
        self.exec()
