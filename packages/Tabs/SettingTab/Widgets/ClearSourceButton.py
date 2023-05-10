from PySide2.QtCore import Signal
from PySide2.QtWidgets import QPushButton

from packages.Startup import GlobalIcons


class ClearSourceButton(QPushButton):
    clear_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setIcon(GlobalIcons.NoMarkIcon)
        self.hint_when_enabled = "Clear"
        self.setToolTip(self.hint_when_enabled)
        self.clicked.connect(self.emit_clear_signal)

    def emit_clear_signal(self):
        self.clear_signal.emit()
