from PySide2.QtCore import Signal
from PySide2.QtWidgets import QPushButton


class PresetTabSetDefaultButton(QPushButton):
    set_active_preset_signal = Signal()

    def __init__(self):
        super().__init__()
        self.set_as_active_text = "Set As Default"
        self.setText(self.set_as_active_text)
        self.hint_when_enabled = "set as default preset for next start"
        self.update_hint()
        self.clicked.connect(self.set_active_preset_signal.emit)
        self.set_disabled()

    def update_hint(self):
        self.setToolTip(self.hint_when_enabled)

    def set_activated(self):
        self.setEnabled(True)
        self.hint_when_enabled = "set as default preset for next start"
        self.update_hint()

    def set_disabled(self):
        self.setEnabled(False)
        self.hint_when_enabled = "already set as default"
        self.update_hint()
