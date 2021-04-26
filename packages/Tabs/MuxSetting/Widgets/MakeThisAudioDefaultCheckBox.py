from PySide2 import QtCore
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QCheckBox, QSizePolicy

from packages.Tabs.GlobalSetting import GlobalSetting


class MakeThisAudioDefaultCheckBox(QCheckBox):
    disable_combo_box = QtCore.Signal(bool)

    def __init__(self):
        super().__init__()
        self.setText("Make This Audio Default  : ")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.setTristate(True)
        self.set_tool_tip_hint_no_check()
        self.stateChanged.connect(self.state_changed)
        self.hint_when_enabled = ""

    def set_tool_tip_hint_no_check(self):
        self.setToolTip(
            "<nobr>Partially checked means the audio track will only be set default<br>Full checked means the audio "
            "track will be set default and forced")
        self.setToolTipDuration(12000)

    def set_tool_tip_hint_partially_check(self):
        self.setToolTip(
            "<nobr>Partially checked means the audio track will only be set default <b>(Activated)</b><br>Full "
            "checked means the audio track will be set default and forced")
        self.setToolTipDuration(12000)

    def set_tool_tip_hint_full_check(self):
        self.setToolTip(
            "<nobr>Partially checked means the audio track will only be set default<br>Full checked means the audio "
            "track will be set default and forced <b>(Activated)</b>")
        self.setToolTipDuration(12000)

    def state_changed(self, state):
        if state == Qt.Unchecked:
            self.disable_combo_box.emit(True)
            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED = False
            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED = False
            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_TRACK = ""
            self.set_tool_tip_hint_no_check()
        else:
            self.disable_combo_box.emit(False)
            if state == Qt.Checked:
                self.set_tool_tip_hint_full_check()
                GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED = False
                GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED = True
            else:
                self.set_tool_tip_hint_partially_check()
                GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED = True
                GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED = False

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
