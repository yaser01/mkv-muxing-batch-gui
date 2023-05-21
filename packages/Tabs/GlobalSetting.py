# Here we have everything that must be shared between all tabs
import hashlib
import json
import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from PySide2.QtWidgets import QWidget

from packages.Startup import GlobalFiles
from packages.Startup.PreDefined import ISO_639_2_SYMBOLS


def convert_string_integer_to_two_digit_string(value):
    s = str(value)
    if len(s) >= 2:
        return s
    else:
        return "0" + s


def get_attribute(data, attribute, default_value):
    return data.get(attribute) or default_value


def sort_names_like_windows(names_list):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(names_list, key=alphanum_key)


def generate_track_ids(ids_list):
    res = []
    for i in ids_list:
        res.append("Track " + str(i))
    return res


def get_readable_filesize(size_bytes, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(size_bytes) < 1024.0:
            return "%3.2f %s%s" % (size_bytes, unit, suffix)
        size_bytes /= 1024.0
    return "%.2f %s%s" % (size_bytes, 'Y', suffix)


def get_files_names_absolute_list(files_names, folder_path):
    result = []
    for i in range(len(files_names)):
        result.append(get_file_name_absolute_path(file_name=files_names[i], folder_path=folder_path))
    return result


def get_file_name_absolute_path(file_name, folder_path):
    return os.path.join(Path(folder_path), file_name)


def write_to_log_file(exception):
    with open(GlobalFiles.AppLogFilePath, 'a+', encoding="UTF-8") as log_file:
        log_file.write(str(datetime.utcnow()) + ' ' + str(exception) + '\n')


def refresh_tracks(track_type):
    videos = GlobalSetting.VIDEO_FILES_ABSOLUTE_PATH_LIST.copy()
    new_list = []
    audios_track_ids = []
    audios_track_languages = []
    audios_track_names = []
    for video_name in videos:
        string_name_hash = hashlib.sha1((str(video_name)).encode('utf-8')).hexdigest()
        media_info_file_path = os.path.join(GlobalFiles.MediaInfoFolderPath, string_name_hash + ".json")
        with open(media_info_file_path, 'r', encoding="UTF-8") as media_info_file:
            json_info = json.load(media_info_file)
        tracks_json_info = json_info["tracks"]
        for track in tracks_json_info:
            if track["type"] == track_type:
                audios_track_ids.append(str(track["id"]))
                language = str(
                    get_attribute(data=track["properties"], attribute="language", default_value="UND"))
                language_symbol = language.lower()
                audios_track_languages.append(ISO_639_2_SYMBOLS.get(language_symbol, "Undetermined"))
                name = str(get_attribute(data=track["properties"], attribute="track_name",
                                         default_value="UnNamedTrackBeBo"))
                if name != "UnNamedTrackBeBo":
                    audios_track_names.append(name)

    audios_track_ids = list(dict.fromkeys(audios_track_ids))
    audios_track_languages = list(dict.fromkeys(audios_track_languages))
    audios_track_names = list(dict.fromkeys(audios_track_names))
    for i in range(len(audios_track_ids)):
        audios_track_ids[i] = convert_string_integer_to_two_digit_string(audios_track_ids[i])
    audios_track_ids.sort()
    audios_track_languages.sort()
    audios_track_names.sort()
    if len(audios_track_ids) > 0:
        new_list = ["---Track Id---"]
        new_list.extend(generate_track_ids(audios_track_ids))
    if len(audios_track_languages) > 0:
        new_list.append("---Language---")
        new_list.extend(audios_track_languages)
    if len(audios_track_names) > 0:
        new_list.append("---Track Name---")
        new_list.extend(audios_track_names)
    return new_list


class GlobalSetting(QWidget):
    LAST_DIRECTORY_PATH = ""
    VIDEO_SOURCE_PATHS = []
    VIDEO_FILES_LIST = []
    VIDEO_FILES_SIZE_LIST = []
    VIDEO_FILES_ABSOLUTE_PATH_LIST = []
    VIDEO_SOURCE_MKV_ONLY = []
    VIDEO_DEFAULT_DURATION_FPS = ""

    SUBTITLE_ENABLED = False
    SUBTITLE_TAB_ENABLED = defaultdict(bool)
    SUBTITLE_FILES_LIST = defaultdict(list)
    SUBTITLE_FILES_ABSOLUTE_PATH_LIST = defaultdict(list)
    SUBTITLE_TRACK_NAME = defaultdict(str)
    SUBTITLE_DELAY = defaultdict(float)
    SUBTITLE_SET_DEFAULT = defaultdict(bool)
    SUBTITLE_SET_FORCED = defaultdict(bool)
    SUBTITLE_SET_AT_TOP = defaultdict(bool)
    SUBTITLE_SET_DEFAULT_DISABLED = False
    SUBTITLE_SET_FORCED_DISABLED = False
    SUBTITLE_LANGUAGE = defaultdict(str)

    AUDIO_ENABLED = False
    AUDIO_TAB_ENABLED = defaultdict(bool)
    AUDIO_FILES_LIST = defaultdict(list)
    AUDIO_FILES_ABSOLUTE_PATH_LIST = defaultdict(list)
    AUDIO_TRACK_NAME = defaultdict(str)
    AUDIO_DELAY = defaultdict(float)
    AUDIO_SET_DEFAULT = defaultdict(bool)
    AUDIO_SET_FORCED = defaultdict(bool)
    AUDIO_SET_AT_TOP = defaultdict(bool)
    AUDIO_SET_DEFAULT_DISABLED = False
    AUDIO_SET_FORCED_DISABLED = False
    AUDIO_LANGUAGE = defaultdict(str)

    ATTACHMENT_ENABLED = False
    ATTACHMENT_FILES_LIST = []
    ATTACHMENT_FILES_CHECKING_LIST = []
    ATTACHMENT_FILES_ABSOLUTE_PATH_LIST = []
    ATTACHMENT_DISCARD_OLD = False

    CHAPTER_ENABLED = False
    CHAPTER_FILES_LIST = []
    CHAPTER_FILES_ABSOLUTE_PATH_LIST = []
    CHAPTER_DISCARD_OLD = False

    MUX_SETTING_AUDIO_TRACKS_LIST = []
    MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_ENABLED = False
    MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_IDS = []
    MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_LANGUAGES = []
    MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_NAMES = []

    MUX_SETTING_SUBTITLE_TRACKS_LIST = []
    MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_ENABLED = False
    MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_IDS = []
    MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_LANGUAGES = []
    MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_NAMES = []

    MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED = False
    MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED = False
    MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_TRACK = ""

    MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_SEMI_ENABLED = False
    MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_FULL_ENABLED = False
    MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_TRACK = ""

    MUX_SETTING_ABORT_ON_ERRORS = False
    MUX_SETTING_KEEP_LOG_FILE = False
    MUX_SETTING_ADD_CRC = False
    MUX_SETTING_REMOVE_OLD_CRC = False

    DESTINATION_FOLDER_PATH = ""
    JOB_QUEUE_EMPTY = True
    JOB_QUEUE_FINISHED = False
    MUXING_ON = False
    LogFilePath = ""
    DISABLE_TOOLTIP = "<b>[Disabled]</b> because job queue has unfinished job(s)"

    def __init__(self):
        super().__init__()
