from PySide2.QtCore import Signal
from PySide2.QtWidgets import QPushButton

from packages.Startup import GlobalFiles
from packages.Tabs.GlobalSetting import GlobalSetting


class DeleteSubtitleButton(QPushButton):
    delete_happened_signal = Signal(int)
    selected_row_after_delete = Signal(int)

    def __init__(self):
        super().__init__()
        self.current_index = -1
        self.max_index = -1
        self.hint_when_enabled = ""
        self.setText("Remove")
        self.setIcon(GlobalFiles.TrashIcon)
        self.setup_tool_tip_hint()
        self.clicked.connect(self.clicked_button)

    def clicked_button(self):
        current_index = self.current_index
        if current_index != -1:
            self.delete_happened_signal.emit(current_index)
            self.selected_row_after_delete.emit(current_index)

    def setup_tool_tip_hint(self):
        self.setToolTip("Remove Subtitle (Delete)")
        self.setToolTipDuration(3000)

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
