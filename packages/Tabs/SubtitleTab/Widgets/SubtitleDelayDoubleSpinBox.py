from PySide2.QtWidgets import QDoubleSpinBox

from packages.Startup.InitializeScreenResolution import screen_size
from packages.Tabs.GlobalSetting import GlobalSetting


class SubtitleDelayDoubleSpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()
        self.hint_when_enabled = ""
        self.setValue(0)
        self.setDecimals(3)
        self.setMinimum(-9999.0)
        self.setMaximum(9999.0)
        self.setSingleStep(0.5)
        self.setMaximumWidth(screen_size.width() // 16)
        self.setToolTip("Subtitle Delay in second(s)")
        self.editingFinished.connect(self.change_global_subtitle_delay)

    def change_global_subtitle_delay(self):
        GlobalSetting.SUBTITLE_DELAY = round(self.value(), 5)

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
