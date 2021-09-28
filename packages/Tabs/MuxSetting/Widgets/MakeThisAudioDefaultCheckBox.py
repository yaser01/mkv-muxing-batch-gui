from PySide2 import QtCore
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QCheckBox, QSizePolicy

from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.MuxSetting.Widgets.ConfirmCheckMakeThisTrackDefault import ConfirmCheckMakeThisTrackDefault
from packages.Tabs.MuxSetting.Widgets.ConfirmCheckMakeThisTrackDefaultWithUnCheckOption import \
    ConfirmCheckMakeThisTrackDefaultWithUnCheckOption


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
        self.stop_check = False

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
        if not self.stop_check:
            audio_to_be_default = -1
            audio_to_be_forced = -1
            for i in GlobalSetting.AUDIO_SET_DEFAULT.keys():
                if GlobalSetting.AUDIO_SET_DEFAULT[i]:
                    audio_to_be_default = i
            for i in GlobalSetting.AUDIO_SET_FORCED.keys():
                if GlobalSetting.AUDIO_SET_FORCED[i]:
                    audio_to_be_forced = i

            if state == Qt.Unchecked:
                self.disable_combo_box.emit(True)
                self.set_tool_tip_hint_no_check()
                GlobalSetting.AUDIO_SET_DEFAULT_DISABLED = False
                GlobalSetting.AUDIO_SET_FORCED_DISABLED = False
                GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED = False
                GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED = False
                GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_TRACK = ""
            else:
                if state == Qt.Checked:
                    if audio_to_be_default != -1 or audio_to_be_forced != -1:
                        confirm_dialog = ConfirmCheckMakeThisTrackDefaultWithUnCheckOption(track_type="audio")
                        confirm_dialog.execute()
                        if confirm_dialog.result == "Yes":
                            self.disable_combo_box.emit(False)
                            self.set_tool_tip_hint_full_check()
                            if audio_to_be_default != -1:
                                GlobalSetting.AUDIO_SET_DEFAULT[audio_to_be_default] = False
                            if audio_to_be_forced != -1:
                                GlobalSetting.AUDIO_SET_FORCED[audio_to_be_forced] = False
                            GlobalSetting.AUDIO_SET_DEFAULT_DISABLED = True
                            GlobalSetting.AUDIO_SET_FORCED_DISABLED = True
                            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED = False
                            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED = True
                        elif confirm_dialog.result == "No":
                            print("ENTER HERE")
                            self.stop_check = True
                            self.disable_combo_box.emit(False)
                            self.setCheckState(Qt.PartiallyChecked)
                            self.set_tool_tip_hint_partially_check()
                            if audio_to_be_default != -1:
                                GlobalSetting.AUDIO_SET_DEFAULT[audio_to_be_default] = False
                            GlobalSetting.AUDIO_SET_DEFAULT_DISABLED = True
                            GlobalSetting.AUDIO_SET_FORCED_DISABLED = False
                            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED = True
                            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED = False
                            self.stop_check = False
                        else:
                            print("ENTER HERE")
                            self.stop_check = True
                            self.setCheckState(Qt.Unchecked)
                            self.disable_combo_box.emit(True)
                            self.set_tool_tip_hint_no_check()
                            GlobalSetting.AUDIO_SET_DEFAULT_DISABLED = False
                            GlobalSetting.AUDIO_SET_FORCED_DISABLED = False
                            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED = False
                            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED = False
                            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_TRACK = ""
                            self.stop_check = False
                    else:
                        self.disable_combo_box.emit(False)
                        self.set_tool_tip_hint_full_check()
                        if audio_to_be_default != -1:
                            GlobalSetting.AUDIO_SET_DEFAULT[audio_to_be_default] = False
                        if audio_to_be_forced != -1:
                            GlobalSetting.AUDIO_SET_FORCED[audio_to_be_forced] = False
                        GlobalSetting.AUDIO_SET_DEFAULT_DISABLED = True
                        GlobalSetting.AUDIO_SET_FORCED_DISABLED = True
                        GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED = False
                        GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED = True
                else:
                    if audio_to_be_default!=-1:
                        confirm_dialog = ConfirmCheckMakeThisTrackDefault(track_type="audio")
                        confirm_dialog.execute()
                        if confirm_dialog.result == "Yes":
                            self.disable_combo_box.emit(False)
                            self.set_tool_tip_hint_partially_check()
                            if audio_to_be_default != -1:
                                GlobalSetting.AUDIO_SET_DEFAULT[audio_to_be_default] = False
                            GlobalSetting.AUDIO_SET_DEFAULT_DISABLED = True
                            GlobalSetting.AUDIO_SET_FORCED_DISABLED = False
                            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED = True
                            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED = False
                        else:
                            self.setCheckState(Qt.Unchecked)
                            self.set_tool_tip_hint_no_check()
                            GlobalSetting.AUDIO_SET_DEFAULT_DISABLED = False
                            GlobalSetting.AUDIO_SET_FORCED_DISABLED = False
                            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED = False
                            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED = False
                            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_TRACK = ""
                    else:
                        self.disable_combo_box.emit(False)
                        self.set_tool_tip_hint_partially_check()
                        if audio_to_be_default != -1:
                            GlobalSetting.AUDIO_SET_DEFAULT[audio_to_be_default] = False
                        GlobalSetting.AUDIO_SET_DEFAULT_DISABLED = True
                        GlobalSetting.AUDIO_SET_FORCED_DISABLED = False
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
