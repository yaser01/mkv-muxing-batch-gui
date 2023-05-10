from PySide2.QtWidgets import QComboBox

from packages.Startup.DefaultOptions import DefaultOptions
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Startup.PreDefined import AllVideoDefaultDurationFPSLanguages
from packages.Startup.SetupThems import get_dark_palette, get_light_palette
from packages.Tabs.GlobalSetting import GlobalSetting


class VideoDefaultDurationFPSComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.hint_when_enabled = "<nobr>Force the default duration or number of frames per second for a video " \
                                 "<br>Only change " \
                                 "it if you really know what you are doing"
        self.setMinimumWidth(screen_size.width() // 11)
        self.addItems(AllVideoDefaultDurationFPSLanguages)
        self.setCurrentIndex(0)
        self.setMaxVisibleItems(8)
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.currentTextChanged.connect(self.change_global_video_default_duration_fps)
        self.setEnabled(True)

    def change_global_video_default_duration_fps(self):
        if self.currentText() == AllVideoDefaultDurationFPSLanguages[0]:
            GlobalSetting.VIDEO_DEFAULT_DURATION_FPS = ""
        else:
            GlobalSetting.VIDEO_DEFAULT_DURATION_FPS = self.currentText()

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

    def update_theme_mode_state(self):
        if DefaultOptions.Dark_Mode:
            self.setPalette(get_dark_palette())
        else:
            self.setPalette(get_light_palette())
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")

