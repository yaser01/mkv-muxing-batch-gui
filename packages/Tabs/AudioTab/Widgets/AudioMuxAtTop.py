from PySide2.QtGui import Qt
from PySide2.QtWidgets import QCheckBox

from packages.Tabs.GlobalSetting import GlobalSetting


class AudioMuxAtTop(QCheckBox):
    def __init__(self, tab_index):
        super().__init__()
        self.tab_index = tab_index
        self.hint_when_enabled = "<nobr>checking this will lead to make this the <b>*</b>First audio  in the " \
                                 "output file <br>Only check it if you really know what you are doing <br><b>*</b>[" \
                                 "Respecting other audios with the same option] "
        self.setText("Mux At Top")
        self.setToolTip(self.hint_when_enabled)
        self.stateChanged.connect(self.change_global_audio_set_at_top)

    def change_global_audio_set_at_top(self):
        GlobalSetting.AUDIO_SET_AT_TOP[self.tab_index] = self.checkState() == Qt.Checked

    def update_check_state(self):
        self.setChecked(bool(GlobalSetting.AUDIO_SET_AT_TOP[self.tab_index]))
        self.setToolTip(self.hint_when_enabled)
        self.setToolTipDuration(12000)

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
