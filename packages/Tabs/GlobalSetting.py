# Here we have everything that must be shared between all tabs
from datetime import datetime
import os
import re
from pathlib import Path

from PySide2.QtWidgets import QWidget

from packages.Startup import GlobalFiles
from packages.Startup.DefaultOptions import Default_Subtitle_Language


def sort_names_like_windows(names_list):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(names_list, key=alphanum_key)


def get_readable_filesize(size_bytes, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(size_bytes) < 1024.0:
            return "%3.1f %s%s" % (size_bytes, unit, suffix)
        size_bytes /= 1024.0
    return "%.1f %s%s" % (size_bytes, 'Y', suffix)


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


class GlobalSetting(QWidget):
    LAST_DIRECTORY_PATH = ""
    VIDEO_SOURCE_PATHS = []
    VIDEO_FILES_LIST = []
    VIDEO_FILES_SIZE_LIST = []
    VIDEO_FILES_ABSOLUTE_PATH_LIST = []
    VIDEO_SOURCE_MKV_ONLY = []
    SUBTITLE_ENABLED = True
    SUBTITLE_FILES_LIST = []
    SUBTITLE_FILES_ABSOLUTE_PATH_LIST = []
    SUBTITLE_TRACK_NAME = ""
    SUBTITLE_DELAY = 0.0
    SUBTITLE_SET_DEFAULT = False
    SUBTITLE_SET_FORCED = False
    SUBTITLE_SET_DEFAULT_DISABLED = False
    SUBTITLE_SET_FORCED_DISABLED = False
    SUBTITLE_LANGUAGE = Default_Subtitle_Language

    ATTACHMENT_ENABLED = False
    ATTACHMENT_FILES_LIST = []
    ATTACHMENT_FILES_CHECKING_LIST = []
    ATTACHMENT_FILES_ABSOLUTE_PATH_LIST = []
    ATTACHMENT_DISCARD_OLD = False

    CHAPTER_ENABLED = False
    CHAPTER_FILES_LIST = []
    CHAPTER_FILES_ABSOLUTE_PATH_LIST = []

    MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_ENABLED = False
    MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS = []
    MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_LANGUAGES = []

    MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_ENABLED = False
    MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS = []
    MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_LANGUAGES = []

    MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED = False
    MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED = False
    MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_TRACK = ""

    MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_SEMI_ENABLED = False
    MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_FULL_ENABLED = False
    MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_TRACK = ""

    MUX_SETTING_ABORT_ON_ERRORS = False
    MUX_SETTING_KEEP_LOG_FILE = False

    DESTINATION_FOLDER_PATH = ""
    JOB_QUEUE_EMPTY = True
    MUXING_ON = False
    LogFilePath = ""
    DISABLE_TOOLTIP = "<b>[Disabled]</b> because job queue has unfinished job(s)"

    def __init__(self):
        super().__init__()
