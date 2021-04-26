from PySide2.QtGui import Qt
from PySide2.QtWidgets import QCheckBox

from packages.Tabs.GlobalSetting import GlobalSetting


class SubtitleSetDefaultCheckBox(QCheckBox):
    def __init__(self):
        super().__init__()
        self.hint_when_enabled = ""
        self.setText("Set Default")
        self.stateChanged.connect(self.change_global_subtitle_set_default)

    def change_global_subtitle_set_default(self):
        GlobalSetting.SUBTITLE_SET_DEFAULT = self.checkState() == Qt.Checked

    def update_check_state(self):
        self.setChecked(bool(GlobalSetting.SUBTITLE_SET_DEFAULT))
        self.setDisabled(bool(GlobalSetting.SUBTITLE_SET_DEFAULT_DISABLED))

        if self.isEnabled():
            self.setToolTip("<nobr>set the new subtitle to be the default subtitle track "
                            "when play")
            self.setToolTipDuration(12000)
        else:
            self.setToolTip(
                "<nobr>set the new subtitle to be the default subtitle track when play<br><b>Disabled</b> because "
                "option "
                "<b>make this subtitle default</b> is enabled on mux setting tab ")
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
