from packages.Startup import GlobalIcons
from packages.Widgets.MoveToDialog import MoveToDialog


class MoveSubtitleToDialog(MoveToDialog):
    def __init__(self, max_index, current_index, parent=None):
        super().__init__(min=1, max=max_index + 1, parent=parent)
        self.spinBox.setValue(current_index + 1)
        self.setWindowTitle("Mover subtítulo")
        self.setWindowIcon(GlobalIcons.SwitchIcon)
        self.message.setText("Mover este subtítulo a:")
        self.extra_message.setText("(esto reemplazará el subtítulo en el destino)")