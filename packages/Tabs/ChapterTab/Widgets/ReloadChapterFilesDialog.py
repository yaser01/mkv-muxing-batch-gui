from packages.Widgets.YesNoDialog import YesNoDialog


class ReloadChapterFilesDialog(YesNoDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.message.setText(
            "Are you sure ?\nThis will reload all chapter files and will affect current matching")
        self.setWindowTitle("Change Chapter Files")

    def execute(self):
        self.exec()
