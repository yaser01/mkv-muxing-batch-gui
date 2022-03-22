import subprocess
import traceback
import zlib
from os.path import getsize

from PySide2.QtCore import Signal, QObject, QThread

from packages.Startup import GlobalFiles
from packages.Tabs.GlobalSetting import write_to_log_file


def get_file_name_with_mkv_extension(file_name):
    file_extension_start_index = file_name.rfind(".")
    new_file_name_with_mkv_extension = file_name[:file_extension_start_index] + ".mkv"
    return new_file_name_with_mkv_extension


class CalculateCRCProcessWorker(QObject):
    crc_progress_signal = Signal(int)
    crc_result_signal = Signal(str)
    all_finished = Signal()

    def __init__(self, file_name=""):
        super().__init__()
        self.file_name = file_name
        self.progress = 0
        self.chunk_size = 65536
        self.wait = True
        self.stop = False

    def run(self):
        try:
            while not self.stop:
                if not self.wait:
                    file_name = get_file_name_with_mkv_extension(self.file_name)
                    file_size = getsize(file_name)
                    with open(file_name, "rb") as f:
                        checksum = 0
                        current_read = 0
                        current_percent = 0
                        while chunk := f.read(self.chunk_size):
                            current_read += self.chunk_size
                            current_percent = int(min(100 * current_read / file_size, 100))
                            self.crc_progress_signal.emit(current_percent)
                            checksum = zlib.crc32(chunk, checksum)
                        crc_string = format(checksum & 0xFFFFFFFF, '08x').upper()
                        self.crc_result_signal.emit(crc_string)
                    self.wait = True
                else:
                    QThread.msleep(50)
            self.all_finished.emit()
        except Exception as e:
            write_to_log_file(traceback.format_exc())
