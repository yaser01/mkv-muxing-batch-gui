from packages.Startup import GlobalIcons
from packages.Widgets.MoveToDialog import MoveToDialog


class MoveAudioToDialog(MoveToDialog):
    def __init__(self, max_index, current_index):
        super().__init__(min=1, max=max_index + 1)
        self.spinBox.setValue(current_index + 1)
        self.setWindowTitle("Move Audio")
        self.setWindowIcon(GlobalIcons.SwitchIcon)
        self.message.setText("Move this audio to :")
        self.extra_message.setText("(this will replace audio in destination)")
