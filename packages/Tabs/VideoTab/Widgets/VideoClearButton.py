from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton

from packages.Startup import GlobalIcons
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.VideoTab.Widgets.ClearVideoFilesDialog import ClearVideoFilesDialog


class VideoClearButton(QPushButton):
    clear_files_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setIcon(GlobalIcons.NoMarkIcon)
        self.hint_when_enabled = "Clear Files"
        self.setToolTip(self.hint_when_enabled)
        self.is_there_old_files = False
        self.clicked.connect(self.open_clear_files_dialog)

    def set_is_there_old_file(self, new_state):
        self.is_there_old_files = new_state

    def open_clear_files_dialog(self):
        if self.is_there_old_files:
            clear_files_dialog = ClearVideoFilesDialog()
            clear_files_dialog.execute()
            if clear_files_dialog.result == "Yes":
                self.clear_files_signal.emit()

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
