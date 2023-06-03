from PySide2.QtCore import Signal
from PySide2.QtWidgets import QCheckBox


class TrackCheckBoxCell(QCheckBox):
    signal_state_changed = Signal(list)

    def __init__(self, row_id, column_id):
        super().__init__()
        self.setStyleSheet("QCheckBox::indicator {width: 20px;height: 20px;}")
        self.row_id = row_id
        self.column_id = column_id
        self.stateChanged.connect(self.emit_checkbox_changed)

    def emit_checkbox_changed(self, new_state):
        self.signal_state_changed.emit([self.row_id, self.column_id, new_state])
