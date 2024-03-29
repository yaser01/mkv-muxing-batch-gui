from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QPushButton, QApplication

from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.VideoTab.Widgets.ModifyOldTracksDialog import ModifyOldTracksDialog


class ModifyOldTracksButton(QPushButton):
    clicked_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setText("Modify Old Tracks")
        self.hint_when_enabled = "[Expert Mode]"
        self.clicked.connect(self.open_modify_old_tracks_dialog)

    def setEnabled(self, new_state: bool):
        super().setEnabled(new_state)
        if not new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setDisabled(self, new_state: bool):
        super().setDisabled(new_state)
        if new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setToolTip(self, new_tool_tip: str):
        if self.isEnabled() or GlobalSetting.JOB_QUEUE_EMPTY:
            self.hint_when_enabled = new_tool_tip
        super().setToolTip(new_tool_tip)

    def open_modify_old_tracks_dialog(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        modify_old_tracks_dialog = ModifyOldTracksDialog(parent=self)
        QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)
        modify_old_tracks_dialog.execute()
