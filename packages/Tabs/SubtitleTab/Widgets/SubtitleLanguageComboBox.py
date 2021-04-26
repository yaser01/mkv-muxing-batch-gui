from PySide2.QtWidgets import QComboBox

from packages.Startup.DefaultOptions import Default_Subtitle_Language
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Startup.PreDefined import AllSubtitlesLanguages
from packages.Tabs.GlobalSetting import GlobalSetting


class SubtitleLanguageComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.hint_when_enabled = ""
        self.setMinimumWidth(screen_size.width() // 13)
        self.addItems(AllSubtitlesLanguages)
        self.setCurrentIndex(AllSubtitlesLanguages.index(Default_Subtitle_Language))
        self.setMaxVisibleItems(8)
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.currentTextChanged.connect(self.change_global_subtitle_language)

    def change_global_subtitle_language(self):
        GlobalSetting.SUBTITLE_LANGUAGE = self.currentText()

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
