from PySide2.QtCore import Qt

from packages.Startup.InitializeScreenResolution import screen_size
from packages.Startup.PreDefined import AllSubtitlesTracks
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.MuxSetting.Widgets.TracksCheckableComboBox import TracksCheckableComboBox


class SubtitleTracksCheckableComboBox(TracksCheckableComboBox):
    def __init__(self):
        super().__init__()
        self.addItems(AllSubtitlesTracks)
        self.setMinimumWidth(screen_size.width() // 12)
        self.setMaximumWidth(screen_size.width() // 6)
        self.setDisabled(True)
        self.empty_selection_hint_string = "Discard All subtitle tracks from the source file<br>this option will lead to " \
                                           "output video with NO old subtitles<br>[the new subtitle file will exists] "

    def check_box_state_changed(self, state):
        if state == Qt.Checked:
            self.setDisabled(False)
            self.set_tool_tip_hint()
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_ENABLED = True
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_LANGUAGES = self.languages
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS = self.tracks
        else:
            self.setDisabled(True)
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_ENABLED = False
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_LANGUAGES = []
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS = []
