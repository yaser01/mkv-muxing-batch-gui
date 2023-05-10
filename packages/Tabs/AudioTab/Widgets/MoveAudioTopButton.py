from PySide2.QtCore import Signal
from PySide2.QtWidgets import QPushButton

from packages.Startup import GlobalIcons
from packages.Startup.DefaultOptions import DefaultOptions
from packages.Tabs.GlobalSetting import GlobalSetting


class MoveAudioTopButton(QPushButton):
    swap_happened_signal = Signal()
    selected_row_after_swap = Signal(int)
    move_audio_to_top_signal = Signal(int)

    def __init__(self):
        super().__init__()
        self.current_index = -1
        self.max_index = -1
        self.hint_when_enabled = ""
        self.setIcon(GlobalIcons.TopLightIcon)
        self.setup_tool_tip_hint()
        self.clicked.connect(self.clicked_button)
        self.dark_mode_applied = False

    def clicked_button(self):
        current_index = self.current_index
        if current_index != 0 and current_index != -1:
            self.move_audio_to_top_signal.emit(current_index)
            self.swap_happened_signal.emit()
            self.selected_row_after_swap.emit(0)

    def setup_tool_tip_hint(self):
        self.setToolTip("Move Sub To Top (Ctrl+PageUp)")
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

    def paintEvent(self, e):
        super().paintEvent(e)
        if DefaultOptions.Dark_Mode and not self.dark_mode_applied:
            self.setIcon(GlobalIcons.TopDarkIcon)
            self.dark_mode_applied = True
        if not DefaultOptions.Dark_Mode and self.dark_mode_applied:
            self.setIcon(GlobalIcons.TopLightIcon)
            self.dark_mode_applied = False