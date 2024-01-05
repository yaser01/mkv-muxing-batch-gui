from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton

from packages.Startup import GlobalIcons
from packages.Tabs.GlobalSetting import GlobalSetting


class RefreshFilesButton(QPushButton):
    clicked_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setIcon(GlobalIcons.RefreshIcon)
        self.hint_when_enabled = "Refresh Files"
        self.current_path = ""
        self.clicked.connect(self.refresh_files)

    def refresh_files(self):
        self.clicked_signal.emit(self.current_path)

    def setEnabled(self, new_state: bool):
        super().setEnabled(new_state)
        if not new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.hint_when_enabled = "Refresh Files"
            self.setToolTip(self.hint_when_enabled)

    def update_current_path(self, new_path):
        self.current_path = new_path

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
