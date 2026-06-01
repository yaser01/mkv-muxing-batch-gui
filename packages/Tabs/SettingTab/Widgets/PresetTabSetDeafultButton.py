from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton


class PresetTabSetDefaultButton(QPushButton):
    set_active_preset_signal = Signal()

    def __init__(self):
        super().__init__()
        self.set_as_active_text = "Establecer como predeterminado"
        self.setText(self.set_as_active_text)
        self.hint_when_enabled = "establecer como preajuste predeterminado para el próximo inicio"
        self.update_hint()
        self.clicked.connect(self.set_active_preset_signal.emit)
        self.set_disabled()

    def update_hint(self):
        self.setToolTip(self.hint_when_enabled)

    def set_activated(self):
        self.setEnabled(True)
        self.hint_when_enabled = "establecer como preajuste predeterminado para el próximo inicio"
        self.update_hint()

    def set_disabled(self):
        self.setEnabled(False)
        self.hint_when_enabled = "ya está establecido como predeterminado"
        self.update_hint()