from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox

from packages.Startup.Options import Options
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Tabs.GlobalSetting import GlobalSetting


class SubtitleLanguageComboBox(QComboBox):
    def __init__(self, tab_index):
        super().__init__()
        self.tab_index = tab_index
        self.hint_when_enabled = ""
        self.setMinimumWidth(screen_size.width() // 13)
        self.addItems(Options.CurrentPreset.Default_Favorite_Subtitle_Languages)
        self.set_current_index()
        self.setToolTip("Subtitle Language: " + Options.CurrentPreset.Default_Subtitle_Language + "\nYou can add/remove "
                                                                                           "languages in options")
        self.setMaxVisibleItems(8)
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.currentTextChanged.connect(self.change_global_subtitle_language)

    def set_current_index(self):
        self.setCurrentIndex(
            Options.CurrentPreset.Default_Favorite_Subtitle_Languages.index(
                Options.CurrentPreset.Default_Subtitle_Language))

    def change_global_subtitle_language(self):
        self.setToolTip("Subtitle Language: " + self.currentText() + "\nYou can add/remove languages in options")
        GlobalSetting.SUBTITLE_LANGUAGE[self.tab_index] = self.currentText()

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

    def addItems(self, texts):
        super().addItems(texts)
        for i in range(len(texts)):
            self.setItemData(i, texts[i], Qt.ItemDataRole.ToolTipRole)
