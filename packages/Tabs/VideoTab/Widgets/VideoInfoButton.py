from PySide2.QtCore import Signal
from PySide2.QtWidgets import QPushButton

from packages.Startup.DefaultOptions import DefaultOptions
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.VideoTab.Widgets.VideoInfoDialog import VideoInfoDialog


class VideoInfoButton(QPushButton):
    clicked_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setText("Media Info")
        self.hint_when_enabled = ""
        self.video_info_dialog = None
        self.is_there_old_files = False
        self.clicked.connect(self.open_video_info_dialog)

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

    def open_video_info_dialog(self):
        if len(GlobalSetting.VIDEO_FILES_ABSOLUTE_PATH_LIST) > 0:
            self.video_info_dialog = VideoInfoDialog()
            self.video_info_dialog.show()

    def update_theme_mode_state(self):
        if self.video_info_dialog is not None:
            self.video_info_dialog.set_dark_mode(DefaultOptions.Dark_Mode)
            self.video_info_dialog.resize(self.video_info_dialog.width(), self.video_info_dialog.height() + 1)
            self.video_info_dialog.resize(self.video_info_dialog.width(), self.video_info_dialog.height() - 1)
