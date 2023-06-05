from PySide2.QtCore import Signal
from PySide2.QtWidgets import QTabWidget

from packages.Startup.PreDefined import AllSubtitlesLanguages, AllAudiosLanguages, AllVideosLanguages
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.VideoTab.Widgets.ModifyOldTracksWidgtes.OldTracksTable import OldTracksTable


class ModifyOldTracksTabsManager(QTabWidget):
    current_selected_track_changed = Signal(list)

    def __init__(self):
        super().__init__()
        self.video_tab = OldTracksTable(
            original_setting=GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_BULK_SETTING_ORIGINAL,
            current_setting=GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_BULK_SETTING,
            tracks_info=GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_INFO,
            all_languages=AllVideosLanguages)
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
        self.addTab(self.video_tab, "Videos")
        self.addTab(self.subtitle_tab, "Subtitles")
        self.addTab(self.audio_tab, "Audios")
        self.video_tab.selected_track_changed.connect(self.update_current_selected_video_track)
        self.subtitle_tab.selected_track_changed.connect(self.update_current_selected_subtitle_track)
        self.audio_tab.selected_track_changed.connect(self.update_current_selected_audio_track)
        self.setCurrentIndex(1)  # current is subtitle tab

    def update_current_selected_video_track(self, new_track_id):
        self.current_selected_track_changed.emit(["video", new_track_id])

    def update_current_selected_subtitle_track(self, new_track_id):
        self.current_selected_track_changed.emit(["subtitle", new_track_id])

    def update_current_selected_audio_track(self, new_track_id):
        self.current_selected_track_changed.emit(["audio", new_track_id])

    def save_settings(self):
        self.video_tab.save_settings()
        self.subtitle_tab.save_settings()
        self.audio_tab.save_settings()
        GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_MODIFIED_ACTIVATED = self.video_tab.is_there_different_track_setting
        GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_REORDER_ACTIVATED = self.video_tab.is_there_reorder_tracks
        GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_DELETED_ACTIVATED = self.video_tab.is_there_deleted_tracks

        GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_MODIFIED_ACTIVATED = self.subtitle_tab.is_there_different_track_setting
        GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_REORDER_ACTIVATED = self.subtitle_tab.is_there_reorder_tracks
        GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_DELETED_ACTIVATED = self.subtitle_tab.is_there_deleted_tracks

        GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_MODIFIED_ACTIVATED = self.audio_tab.is_there_different_track_setting
        GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_REORDER_ACTIVATED = self.audio_tab.is_there_reorder_tracks
        GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_DELETED_ACTIVATED = self.audio_tab.is_there_deleted_tracks

    def restore_defaults(self):
        self.video_tab.restore_defaults()
        self.subtitle_tab.restore_defaults()
        self.audio_tab.restore_defaults()
