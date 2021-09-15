from packages.Widgets.YesNoDialog import YesNoDialog


class ReloadChapterFilesDialog(YesNoDialog):
    def __init__(self):
        super().__init__()
        self.message.setText(
            "Are you sure ?\nThis will reload all chapter files and will affect current matching")
        self.setWindowTitle("Change Chapter Files")

    def execute(self):
        self.exec_()
