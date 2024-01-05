from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton

from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.SubtitleTab.Widgets.MoveSubtitleToDialog import MoveSubtitleToDialog


class MoveSubtitleToButton(QPushButton):
    swap_happened_signal = Signal()
    selected_row_after_swap = Signal(int)
    move_subtitle_to_position_signal = Signal(list)

    def __init__(self):
        super().__init__()
        self.current_index = -1
        self.max_index = -1
        self.setText("Move To")
        self.hint_when_enabled = ""
        self.setup_tool_tip_hint()
        self.clicked.connect(self.clicked_button)

    def clicked_button(self):
        current_index = self.current_index
        if current_index != -1:
            move_subtitle_to_dialog = MoveSubtitleToDialog(max_index=self.max_index, current_index=current_index,
                                                           parent=self)
            move_subtitle_to_dialog.execute()
            if move_subtitle_to_dialog.result == "Yes":
                new_index = move_subtitle_to_dialog.position - 1
                self.move_subtitle_to_position_signal.emit([current_index, new_index])
                self.swap_happened_signal.emit()
                self.selected_row_after_swap.emit(new_index)

    def setup_tool_tip_hint(self):
        self.setToolTip("Move To")
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
