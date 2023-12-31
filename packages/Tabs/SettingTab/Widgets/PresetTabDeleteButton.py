from PySide2.QtCore import Signal
from PySide2.QtWidgets import QPushButton
from packages.Startup import GlobalIcons
from packages.Startup.Options import Options


class PresetTabDeleteButton(QPushButton):
    remove_tab_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setIcon(GlobalIcons.TrashLightIcon)
        self.hint_when_enabled = "Delete Preset"
        self.setToolTip(self.hint_when_enabled)
        self.clicked.connect(self.remove_tab_signal.emit)
        self.dark_mode_applied = False

    def paintEvent(self, e):
        super().paintEvent(e)
        if Options.Dark_Mode and not self.dark_mode_applied:
            self.setIcon(GlobalIcons.TrashDarkIcon)
            self.dark_mode_applied = True
        if not Options.Dark_Mode and self.dark_mode_applied:
            self.setIcon(GlobalIcons.TrashLightIcon)
            self.dark_mode_applied = False
