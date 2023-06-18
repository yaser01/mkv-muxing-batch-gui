from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QCheckBox

from packages.Startup.Options import Options, save_options
from packages.Tabs.AttachmentTab.Widgets.SwitchingToExpertModeDialog import SwitchingToExpertModeDialog
from packages.Tabs.GlobalSetting import GlobalSetting


class ExpertModeCheckBox(QCheckBox):
    is_checked_signal = Signal(bool)

    def __init__(self):
        super().__init__()
        self.hint_when_enabled = "<nobr>Activating Expert Mode<br>Enable The Ability To Select [File or " \
                                 "Folder] For Each Video <b>Separately</b>"
        self.setText("Expert Mode")
        self.toggled.connect(self.change_global_expert_mode_attachments)
        self.setToolTip(self.hint_when_enabled)
        self.skip_state_changed = False
        self.should_show_expert_mode_info_message = Options.Attachment_Expert_Mode_Info_Message_Show

    # noinspection PyMethodMayBeStatic
    def change_global_expert_mode_attachments(self, new_state):
        if self.skip_state_changed:
            return
        if new_state:
            if self.should_show_expert_mode_info_message:
                confirm_switching_to_expert_mode = SwitchingToExpertModeDialog()
                confirm_switching_to_expert_mode.execute()
                confirm_enter_expert_mode = confirm_switching_to_expert_mode.result == "Expert"
                self.should_show_expert_mode_info_message = confirm_switching_to_expert_mode.show_message_result == "Yes"
                if confirm_enter_expert_mode:
                    GlobalSetting.ATTACHMENT_EXPERT_MODE = new_state
                    self.is_checked_signal.emit(new_state)
                else:
                    self.skip_state_changed = True
                    self.setCheckState(Qt.Unchecked)
                    self.skip_state_changed = False
            else:
                GlobalSetting.ATTACHMENT_EXPERT_MODE = new_state
                self.is_checked_signal.emit(new_state)
        else:
            GlobalSetting.ATTACHMENT_EXPERT_MODE = new_state
            self.is_checked_signal.emit(new_state)
        Options.Attachment_Expert_Mode_Info_Message_Show = self.should_show_expert_mode_info_message
        save_options()

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
