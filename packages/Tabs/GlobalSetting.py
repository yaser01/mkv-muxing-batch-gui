# Here we have everything that must be shared between all tabs
import copy
import hashlib
import json
import logging
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget

from packages.Startup import GlobalFiles
from packages.Startup.PreDefined import ISO_639_2_SYMBOLS
from packages.Widgets.PathData import PathData
from packages.Widgets.SingleOldTrackData import SingleOldTrackData


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


def convert_string_to_boolean(string):
    if string in ["True", "true", "T", "t"]:
        return True
    else:
        return False


def convert_boolean_to_checked_value(value):
    if value is None:
        return 1  # Qt.PartiallyChecked
    if value:
        return 2  # Qt.Checked
    return 0  # Qt.Unchecked


def convert_check_state_int_to_check_state(value):
    if value == 1:
        return Qt.PartiallyChecked
    if value == 2:
        return Qt.Checked
    return Qt.Unchecked


def write_to_log_file(exception):
    logging.error(exception)


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


def refresh_old_tracks_info_as_bulk(tracks_info: List[List[SingleOldTrackData]]):
    tracks_bulk_data = defaultdict(SingleOldTrackData)
    track_dict = {}
    for video_id, tracks_list in enumerate(tracks_info, start=1):
        for track in tracks_list:
            track_id = track.id
            if track_id not in track_dict.keys():
                track_dict[track_id] = defaultdict(SingleOldTrackData)
            single_old_track_data: SingleOldTrackData = SingleOldTrackData()
            single_old_track_data.id = track_id
            single_old_track_data.track_name = track.track_name
            single_old_track_data.language = track.language
            single_old_track_data.is_default = track.is_default
            single_old_track_data.is_forced = track.is_forced
            single_old_track_data.is_enabled = track.is_enabled
            track_dict[track_id][video_id] = single_old_track_data
            # print(video_id)
            # print(single_old_track_data.id, " # ", single_old_track_data.track_name, " # ",
            #       single_old_track_data.language, " # ", single_old_track_data.is_enabled, " # ",
            #       single_old_track_data.is_default, " # ", single_old_track_data.is_forced, " # ")

    for order_id, track_id in enumerate(track_dict.keys()):
        temp_old_track_data = SingleOldTrackData()
        all_same = True
        for video_id in track_dict[track_id]:
            if temp_old_track_data.id == "":
                temp_old_track_data = track_dict[track_id][video_id]
            else:
                if temp_old_track_data.track_name != track_dict[track_id][video_id].track_name:
                    temp_old_track_data.track_name = "[Old]"
                if temp_old_track_data.language != track_dict[track_id][video_id].language:
                    temp_old_track_data.language = "[Old]"
                if temp_old_track_data.is_enabled != track_dict[track_id][video_id].is_enabled:
                    temp_old_track_data.is_enabled = None
                if temp_old_track_data.is_default != track_dict[track_id][video_id].is_default:
                    temp_old_track_data.is_default = None
                if temp_old_track_data.is_forced != track_dict[track_id][video_id].is_forced:
                    temp_old_track_data.is_forced = None
        if all_same:
            tracks_bulk_data[track_id] = temp_old_track_data
        else:
            temp_old_track_data.track_name = "[Old]"
            temp_old_track_data.language = "[Old]"
            tracks_bulk_data[track_id] = temp_old_track_data
        tracks_bulk_data[track_id].is_enabled = convert_boolean_to_checked_value(tracks_bulk_data[track_id].is_enabled)
        tracks_bulk_data[track_id].is_default = convert_boolean_to_checked_value(tracks_bulk_data[track_id].is_default)
        tracks_bulk_data[track_id].is_forced = convert_boolean_to_checked_value(tracks_bulk_data[track_id].is_forced)
        tracks_bulk_data[track_id].order = order_id
    return tracks_bulk_data


def refresh_old_tracks_info(track_type):
    videos = GlobalSetting.VIDEO_FILES_ABSOLUTE_PATH_LIST.copy()
    new_list: List[List[SingleOldTrackData]] = []
    for video_name in videos:
        video_tracks: List[SingleOldTrackData] = []
        string_name_hash = hashlib.sha1((str(video_name)).encode('utf-8')).hexdigest()
        media_info_file_path = os.path.join(GlobalFiles.MediaInfoFolderPath, string_name_hash + ".json")
        with open(media_info_file_path, 'r', encoding="UTF-8") as media_info_file:
            json_info = json.load(media_info_file)
        tracks_json_info = json_info["tracks"]
        for track in tracks_json_info:
            new_track: SingleOldTrackData = SingleOldTrackData()
            if track["type"] == track_type:
                new_track.id = str(track["id"])
                language = str(
                    get_attribute(data=track["properties"], attribute="language", default_value="UND"))
                language_symbol = language.lower()
                new_track.language = ISO_639_2_SYMBOLS.get(language_symbol, "Undetermined")
                name = str(get_attribute(data=track["properties"], attribute="track_name",
                                         default_value="UnNamedTrackBeBo"))
                if name != "UnNamedTrackBeBo":
                    new_track.track_name = name
                new_track.is_default = get_attribute(data=track["properties"], attribute="default_track",
                                                     default_value=False)
                new_track.is_forced = get_attribute(data=track["properties"], attribute="forced_track",
                                                    default_value=False)
                new_track.is_enabled = True
                new_track.uid = str(
                    get_attribute(data=track["properties"], attribute="uid", default_value="-1"))
                video_tracks.append(new_track)
        new_list.append(video_tracks)
    if track_type == "audio":
        GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_INFO = new_list
        GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING_ORIGINAL = refresh_old_tracks_info_as_bulk(
            tracks_info=GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_INFO)
        GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING = copy.deepcopy(
            GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING_ORIGINAL)
    elif track_type == "subtitles":
        GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_INFO = new_list
        GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING_ORIGINAL = refresh_old_tracks_info_as_bulk(
            tracks_info=GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_INFO)
        GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING = copy.deepcopy(
            GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING_ORIGINAL)
    elif track_type == "video":
        GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_INFO = new_list
        GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_BULK_SETTING_ORIGINAL = refresh_old_tracks_info_as_bulk(
            tracks_info=GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_INFO)
        GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_BULK_SETTING = copy.deepcopy(
            GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_BULK_SETTING_ORIGINAL)


class GlobalSetting(QWidget):
    LAST_DIRECTORY_PATH = ""
    VIDEO_SOURCE_PATHS = []
    VIDEO_FILES_LIST = []
    VIDEO_FILES_SIZE_LIST = []
    VIDEO_FILES_ABSOLUTE_PATH_LIST = []
    VIDEO_SOURCE_MKV_ONLY = False
    VIDEO_DEFAULT_DURATION_FPS = ""
    VIDEO_OLD_TRACKS_VIDEOS_INFO: List[List[SingleOldTrackData]] = []
    VIDEO_OLD_TRACKS_AUDIOS_INFO: List[List[SingleOldTrackData]] = []
    VIDEO_OLD_TRACKS_SUBTITLES_INFO: List[List[SingleOldTrackData]] = []
    VIDEO_OLD_TRACKS_VIDEOS_BULK_SETTING_ORIGINAL = defaultdict(SingleOldTrackData)
    VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING_ORIGINAL = defaultdict(SingleOldTrackData)
    VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING_ORIGINAL = defaultdict(SingleOldTrackData)
    VIDEO_OLD_TRACKS_VIDEOS_BULK_SETTING = defaultdict(SingleOldTrackData)
    VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING = defaultdict(SingleOldTrackData)
    VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING = defaultdict(SingleOldTrackData)
    VIDEO_OLD_TRACKS_VIDEOS_MODIFIED_ACTIVATED = False
    VIDEO_OLD_TRACKS_VIDEOS_REORDER_ACTIVATED = False
    VIDEO_OLD_TRACKS_VIDEOS_DELETED_ACTIVATED = False
    VIDEO_OLD_TRACKS_SUBTITLES_MODIFIED_ACTIVATED = False
    VIDEO_OLD_TRACKS_SUBTITLES_REORDER_ACTIVATED = False
    VIDEO_OLD_TRACKS_SUBTITLES_DELETED_ACTIVATED = False
    VIDEO_OLD_TRACKS_AUDIOS_MODIFIED_ACTIVATED = False
    VIDEO_OLD_TRACKS_AUDIOS_REORDER_ACTIVATED = False
    VIDEO_OLD_TRACKS_AUDIOS_DELETED_ACTIVATED = False

    SUBTITLE_ENABLED = False
    SUBTITLE_TAB_ENABLED = defaultdict(bool)
    SUBTITLE_FILES_LIST = defaultdict(list)
    SUBTITLE_FILES_ABSOLUTE_PATH_LIST = defaultdict(list)
    SUBTITLE_TRACK_NAME = defaultdict(str)
    SUBTITLE_DELAY = defaultdict(float)
    SUBTITLE_SET_DEFAULT = defaultdict(bool)
    SUBTITLE_SET_FORCED = defaultdict(bool)
    SUBTITLE_SET_ORDER = defaultdict(int)
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
    AUDIO_SET_ORDER = defaultdict(int)
    AUDIO_SET_DEFAULT_DISABLED = False
    AUDIO_SET_FORCED_DISABLED = False
    AUDIO_LANGUAGE = defaultdict(str)

    ATTACHMENT_ENABLED = False
    ATTACHMENT_FILES_LIST = []
    ATTACHMENT_FILES_CHECKING_LIST = []
    ATTACHMENT_FILES_ABSOLUTE_PATH_LIST = []
    ATTACHMENT_DISCARD_OLD = False
    ATTACHMENT_ALLOW_DUPLICATE = False

    ATTACHMENT_EXPERT_MODE = False
    ATTACHMENT_PATH_DATA_LIST: List[PathData] = []

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
    OVERWRITE_SOURCE_FILES = False
    RANDOM_OUTPUT_SUFFIX = ""
    USE_MKVPROPEDIT = False

    JOB_QUEUE_EMPTY = True
    JOB_QUEUE_FINISHED = False
    MUXING_ON = False
    LogFilePath = ""
    DISABLE_TOOLTIP = "<b>[Disabled]</b> because job queue has unfinished job(s)"
    def __init__(self):
        super().__init__()
