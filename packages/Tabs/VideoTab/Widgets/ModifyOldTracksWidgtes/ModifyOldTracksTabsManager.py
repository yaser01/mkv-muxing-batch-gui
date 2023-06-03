from PySide2.QtCore import Signal
from PySide2.QtWidgets import QTabWidget

from packages.Startup.PreDefined import AllSubtitlesLanguages, AllAudiosLanguages
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.VideoTab.Widgets.ModifyOldTracksWidgtes.OldTracksTable import OldTracksTable


class ModifyOldTracksTabsManager(QTabWidget):
    current_selected_track_changed = Signal(list)

    def __init__(self):
        super().__init__()
        self.subtitle_tab = OldTracksTable(
            original_setting=GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING_ORIGINAL,
            current_setting=GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING,
            tracks_info=GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_INFO,
            all_languages=AllSubtitlesLanguages)
        self.audio_tab = OldTracksTable(
            original_setting=GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING_ORIGINAL,
            current_setting=GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING,
            tracks_info=GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_INFO,
            all_languages=AllAudiosLanguages)
        self.addTab(self.subtitle_tab, "Subtitles")
        self.addTab(self.audio_tab, "Audios")
        self.subtitle_tab.selected_track_changed.connect(self.update_current_selected_subtitle_track)
        self.audio_tab.selected_track_changed.connect(self.update_current_selected_audio_track)

    def update_current_selected_subtitle_track(self, new_track_id):
        self.current_selected_track_changed.emit(["subtitle", new_track_id])

    def update_current_selected_audio_track(self, new_track_id):
        self.current_selected_track_changed.emit(["audio", new_track_id])

    def save_settings(self):
        self.subtitle_tab.save_settings()
        self.audio_tab.save_settings()
        if self.subtitle_tab.is_there_different_track_setting or self.audio_tab.is_there_different_track_setting:
            GlobalSetting.VIDEO_OLD_TRACKS_ACTIVATED = True
        else:
            GlobalSetting.VIDEO_OLD_TRACKS_ACTIVATED = False

    def restore_defaults(self):
        self.subtitle_tab.restore_defaults()
        self.audio_tab.restore_defaults()
