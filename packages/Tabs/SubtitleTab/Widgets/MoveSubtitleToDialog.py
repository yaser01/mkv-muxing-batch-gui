from packages.Startup import GlobalFiles
from packages.Widgets.MoveToDialog import MoveToDialog


class MoveSubtitleToDialog(MoveToDialog):
    def __init__(self, max_index, current_index):
        super().__init__(min=1, max=max_index + 1)
        self.spinBox.setValue(current_index + 1)
        self.setWindowTitle("Move Subtitle")
        self.setWindowIcon(GlobalFiles.SwitchIcon)
        self.message.setText("Move this subtitle to :")
        self.extra_message.setText("(this will replace subtitle in destination)")
