from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QComboBox

from packages.Tabs.GlobalSetting import GlobalSetting


def append_int(num):
    if num > 9:
        secondToLastDigit = str(num)[-2]
        if secondToLastDigit == '1':
            return 'th'
    lastDigit = num % 10
    if lastDigit == 1:
        return 'st'
    elif lastDigit == 2:
        return 'nd'
    elif lastDigit == 3:
        return 'rd'
    else:
        return 'th'


def num_to_ith(num):
    value = str(num) + append_int(num)
    return value


class AudioMuxAfterTracksComboBox(QComboBox):
    current_index_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.hint_when_enabled = ""
        self.setMaxVisibleItems(8)
        self.setMinimumWidth(100)
        self.currentIndexChanged.connect(self.current_index_changed.emit)

    def update_tracks(self, number_of_tracks):
        self.clear()
        self.addItem("[At Top]")
        for item_id in range(1, number_of_tracks + 1):
            self.addItem(num_to_ith(item_id) + " Audio")
        for i in range(self.count()):
            self.setItemData(i, self.itemText(i), Qt.ItemDataRole.ToolTipRole)
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.setCurrentIndex(0)

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
