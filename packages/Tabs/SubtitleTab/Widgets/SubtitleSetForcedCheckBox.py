from PySide2.QtGui import Qt
from PySide2.QtWidgets import QCheckBox

from packages.Tabs.GlobalSetting import GlobalSetting


class SubtitleSetForcedCheckBox(QCheckBox):
    def __init__(self, tab_index):
        super().__init__()
        self.tab_index = tab_index
        self.hint_when_enabled = ""
        self.setText("Set Forced")
        self.stateChanged.connect(self.change_global_subtitle_set_forced)

    def change_global_subtitle_set_forced(self):
        GlobalSetting.SUBTITLE_SET_FORCED[self.tab_index] = self.checkState() == Qt.CheckState.Checked
        if self.checkState() == Qt.CheckState.Checked:
            for i in GlobalSetting.SUBTITLE_SET_FORCED.keys():

                if i != self.tab_index:
                    GlobalSetting.SUBTITLE_SET_FORCED[i] = False

    def update_check_state(self):
        self.setChecked(bool(GlobalSetting.SUBTITLE_SET_FORCED[self.tab_index]))
        self.setDisabled(bool(GlobalSetting.SUBTITLE_SET_FORCED_DISABLED))

        if self.isEnabled():
            self.setToolTip("<nobr>set the new subtitle to be the forced subtitle track when "
                            "play")
            self.setToolTipDuration(12000)
        else:
            self.setToolTip(
                "<nobr>set the new subtitle to be the forced subtitle track when play<br><b>Disabled</b> because "
                "option "
                "<b>make this subtitle default and forced</b> is enabled on mux setting tab ")
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
