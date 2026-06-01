import hashlib
import json
import subprocess
import time
import traceback
from pathlib import Path

from PySide6.QtCore import QObject, Signal

from packages.Startup import GlobalFiles
from packages.Tabs.GlobalSetting import write_to_log_file


def add_two_spaces():
    return "  "


def add_double_quotation(string):
    return add_two_spaces() + '"' + str(string) + '"'


def get_attribute(data, attribute, default_value):
    return data.get(attribute) or default_value


def check_if_valid_video_input(file_name: Path):
    string_name_hash = hashlib.sha1((str(file_name)).encode("utf-8")).hexdigest()
    media_info_file_path = GlobalFiles.MediaInfoFolderPath / (string_name_hash + ".json")
    with open(media_info_file_path, "r", encoding="utf-8") as media_info_file:
        json_info = json.load(media_info_file)
    tracks_json_info = get_attribute(json_info, "tracks", False)
    if not tracks_json_info:
        return False
    is_valid_video = False
    for track in tracks_json_info:
        if get_attribute(track, "type", "not video") == "video":
            is_valid_video = True
            break
    return is_valid_video


class GenerateMediaInfoFilesWorker(QObject):
    job_succeeded_signal = Signal()
    job_unsupported_file_signal = Signal(str)
    finished_all_jobs_signal = Signal()

    def __init__(self, video_list: list[Path]):
        super().__init__()
        self.video_list = video_list

    def run(self):
        try:
            for file_name in self.video_list:
                string_name_hash = hashlib.sha1(
                    (str(file_name)).encode("utf-8")
                ).hexdigest()
                media_info_file_path = GlobalFiles.MediaInfoFolderPath / (
                    string_name_hash + ".json"
                )
                command = [
                    add_double_quotation(GlobalFiles.MKVMERGE_PATH),
                    " -J ",
                    add_double_quotation(file_name),
                ]
                command = [str(i) for i in command]
                p1 = subprocess.run(
                    " ".join(command),
                    # shell mode for windows
                    shell=True,
                    stdout=subprocess.PIPE,
                    env=GlobalFiles.ENVIRONMENT,
                    text=True,
                    encoding="utf-8",  # Force utf-8 # windows thing
                )
                with open(
                    media_info_file_path, "w+", encoding="utf-8"
                ) as media_info_file:
                    media_info_file.write(p1.stdout.strip())
                time.sleep(0.05)
                if not check_if_valid_video_input(file_name):
                    self.job_unsupported_file_signal.emit(file_name)
                self.job_succeeded_signal.emit()
            self.finished_all_jobs_signal.emit()
        except Exception:
            write_to_log_file(traceback.format_exc())