import hashlib
import os
import subprocess
import time
import traceback

from PySide2.QtCore import QObject, Signal

from packages.Startup import GlobalFiles
from packages.Tabs.GlobalSetting import write_to_log_file


def add_two_spaces():
    return "  "


def add_double_quotation(string):
    return add_two_spaces() + "\"" + str(string) + "\""


class GenerateMediaInfoFilesWorker(QObject):
    job_succeeded_signal = Signal()
    finished_all_jobs_signal = Signal()

    def __init__(self, video_list):
        super().__init__()
        self.video_list = video_list

    def run(self):
        try:
            for file_name in self.video_list:
                string_name_hash = hashlib.sha1((str(file_name)).encode('utf-8')).hexdigest()
                media_info_file_path = os.path.join(GlobalFiles.MediaInfoFolderPath, string_name_hash + ".json")
                with open(media_info_file_path, 'w+', encoding="UTF-8") as media_info_file:
                    command = add_double_quotation(GlobalFiles.MKVMERGE_PATH) + " -J " + add_double_quotation(
                        file_name)
                    subprocess.run(command, shell=True, stdout=media_info_file)
                time.sleep(0.05)
                self.job_succeeded_signal.emit()
            self.finished_all_jobs_signal.emit()
        except Exception as e:
            write_to_log_file(traceback.format_exc())
