from packages.Startup import GlobalIcons
from packages.Widgets.MoveToDialog import MoveToDialog


class MoveAudioToDialog(MoveToDialog):
    def __init__(self, max_index, current_index, parent=None):
        super().__init__(min=1, max=max_index + 1, parent=parent)
        self.spinBox.setValue(current_index + 1)
        self.setWindowTitle("Mover audio")
        self.setWindowIcon(GlobalIcons.SwitchIcon)
        self.message.setText("Mover este audio a:")
        self.extra_message.setText("(esto reemplazará el audio en el destino)")