from packages.Startup import GlobalIcons
from packages.Widgets.YesNoDialog import YesNoDialog


class ClearSubtitleTabDialog(YesNoDialog):
    def __init__(self):
        super().__init__()
        self.message.setText(
            "Are you sure ?\nThis will remove current tab")
        self.setWindowTitle("Remove Tab")
        self.setWindowIcon(GlobalIcons.NoMarkIcon)

    def execute(self):
        self.exec_()
