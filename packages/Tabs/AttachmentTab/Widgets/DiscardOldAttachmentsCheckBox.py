from PySide2.QtWidgets import QCheckBox

from packages.Tabs.GlobalSetting import GlobalSetting


class DiscardOldAttachmentsCheckBox(QCheckBox):
    def __init__(self):
        super().__init__()
        self.hint_when_enabled = ""
        self.setText("Discard Old Attachments ")
        self.toggled.connect(self.change_global_discard_old_attachments)

    # noinspection PyMethodMayBeStatic
    def change_global_discard_old_attachments(self, new_state):
        GlobalSetting.ATTACHMENT_DISCARD_OLD = new_state

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
