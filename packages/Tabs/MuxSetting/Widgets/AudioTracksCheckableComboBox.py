from PySide2.QtCore import Qt
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Startup.PreDefined import AllAudiosTracks
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.MuxSetting.Widgets.TracksCheckableComboBox import TracksCheckableComboBox


class AudioTracksCheckableComboBox(TracksCheckableComboBox):

    def __init__(self):
        super().__init__()
        self.addItems(AllAudiosTracks)
        self.setMinimumWidth(screen_size.width() // 12)
        self.setMaximumWidth(screen_size.width() // 4)
        self.setDisabled(True)
        self.empty_selection_hint_string = "Discard All audio tracks from the source file<br>this option will lead to " \
                                           "output video with NO audios<br>[the new audio file(s) will exists]"

    def check_box_state_changed(self, new_state):
        if new_state == Qt.CheckState.Checked:
            self.setDisabled(False)
            self.set_tool_tip_hint()
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_ENABLED = True
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_LANGUAGES = self.tracks_language
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_IDS = self.tracks_id
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_NAMES = self.tracks_name
        else:
            self.setDisabled(True)
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_ENABLED = False
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_LANGUAGES = []
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_IDS = []
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_NAMES = []

    def refresh_tracks(self):
        new_list = GlobalSetting.MUX_SETTING_AUDIO_TRACKS_LIST
        if new_list != self.current_list:
            self.addItems(new_list)
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_LANGUAGES = []
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_IDS = []
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_NAMES = []
