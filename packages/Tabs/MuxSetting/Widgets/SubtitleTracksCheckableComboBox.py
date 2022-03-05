import hashlib
import json
import os

from PySide2.QtCore import Qt, Signal

from packages.Startup import GlobalFiles
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Startup.PreDefined import AllSubtitlesTracks, ISO_639_2_SYMBOLS
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.MuxSetting.Widgets.TracksCheckableComboBox import TracksCheckableComboBox


def generate_track_ids(ids_list):
    res = []
    for i in ids_list:
        res.append("Track " + str(i))
    return res


def get_attribute(data, attribute, default_value):
    return data.get(attribute) or default_value


def convert_string_integer_to_two_digit_string(value):
    s = str(value)
    if len(s) >= 2:
        return s
    else:
        return "0" + s


class SubtitleTracksCheckableComboBox(TracksCheckableComboBox):
    subtitle_tracks_changed_signal = Signal(list)

    def __init__(self):
        super().__init__()
        self.addItems(AllSubtitlesTracks)
        self.setMinimumWidth(screen_size.width() // 12)
        self.setMaximumWidth(screen_size.width() // 4)
        self.setDisabled(True)
        self.empty_selection_hint_string = "Discard All subtitle tracks from the source file<br>this option will lead to " \
                                           "output video with NO old subtitles<br>[the new subtitle file(s) will exists] "

    def check_box_state_changed(self, state):
        if state == Qt.Checked:
            self.setDisabled(False)
            self.set_tool_tip_hint()
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_ENABLED = True
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_LANGUAGES = self.tracks_language
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_IDS = self.tracks_id
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_NAMES = self.tracks_name
        else:
            self.setDisabled(True)
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_ENABLED = False
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_LANGUAGES = []
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_IDS = []
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_NAMES = []

    def refresh_tracks(self):
        videos = GlobalSetting.VIDEO_FILES_ABSOLUTE_PATH_LIST.copy()
        new_list = []
        subtitles_track_ids = []
        subtitles_track_languages = []
        subtitles_track_names = []
        for video_name in videos:
            string_name_hash = hashlib.sha1((str(video_name)).encode('utf-8')).hexdigest()
            media_info_file_path = os.path.join(GlobalFiles.MediaInfoFolderPath, string_name_hash + ".json")
            with open(media_info_file_path, 'r', encoding="UTF-8") as media_info_file:
                json_info = json.load(media_info_file)
            tracks_json_info = json_info["tracks"]
            for track in tracks_json_info:
                if track["type"] == "subtitles":
                    subtitles_track_ids.append(str(track["id"]))
                    language = str(
                        get_attribute(data=track["properties"], attribute="language", default_value="UND"))
                    language_symbol = language.lower()
                    subtitles_track_languages.append(ISO_639_2_SYMBOLS.get(language_symbol, "Undetermined"))
                    name = str(get_attribute(data=track["properties"], attribute="track_name",
                                             default_value="UnNamedTrackBeBo"))
                    if name != "UnNamedTrackBeBo":
                        subtitles_track_names.append(name)

        subtitles_track_ids = list(dict.fromkeys(subtitles_track_ids))
        subtitles_track_languages = list(dict.fromkeys(subtitles_track_languages))
        subtitles_track_names = list(dict.fromkeys(subtitles_track_names))
        for i in range(len(subtitles_track_ids)):
            subtitles_track_ids[i] = convert_string_integer_to_two_digit_string(subtitles_track_ids[i])
        subtitles_track_ids.sort()
        subtitles_track_languages.sort()
        subtitles_track_names.sort()
        if len(subtitles_track_ids) > 0:
            new_list = ["---Track Id---"]
            new_list.extend(generate_track_ids(subtitles_track_ids))
        if len(subtitles_track_languages) > 0:
            new_list.append("---Language---")
            new_list.extend(subtitles_track_languages)
        if len(subtitles_track_names) > 0:
            new_list.append("---Track Name---")
            new_list.extend(subtitles_track_names)
        if new_list != self.current_list:
            self.addItems(new_list)
            self.subtitle_tracks_changed_signal.emit(new_list)
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_LANGUAGES = []
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_IDS = []
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_NAMES = []
