import time

from PySide2.QtCore import Signal, QObject, QThread

from packages.Startup import GlobalFiles
from packages.Tabs.MuxSetting.Widgets.MuxingParams import MuxingParams


def next_line(file):
    file.seek(0, 2)  # go to the end of file
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.05)
        else:
            yield line


def get_int_from_string(string):
    string_digits = ''.join(x for x in string if x.isdigit())
    return int(string_digits)


class ReadFromMkvmergeLogWorker(QObject):
    finished_job_signal = Signal(str)
    all_finished = Signal()
    send_muxing_progress_data_signal = Signal(MuxingParams)

    def __init__(self, job_index):
        super().__init__()
        self.job_index = job_index
        self.wait = True
        self.stop = False

    def run(self):
        while not self.stop:
            if not self.wait:
                muxing_params = MuxingParams()
                muxing_params.index = self.job_index
                muxing_params.progress = 0
                with open(GlobalFiles.LogFilePath, "a+") as log_file:
                    for line in next_line(log_file):
                        if line.find('Progress:') != -1:
                            new_progress = get_int_from_string(line)
                            muxing_params.progress = new_progress
                            self.send_muxing_progress_data_signal.emit(muxing_params)
                        elif line.find('Error in the Matroska file structure') != -1:
                            muxing_params.error = True
                            muxing_params.message = line
                            self.send_muxing_progress_data_signal.emit(muxing_params)
                        elif line.find('Multiplexing took') != -1:
                            muxing_params.progress = 100
                            self.send_muxing_progress_data_signal.emit(muxing_params)
                            break
                        elif line.find("Error: ") != -1:
                            muxing_params.error = True
                            muxing_params.message = line
                            self.send_muxing_progress_data_signal.emit(muxing_params)
                            break
                self.finished_job_signal.emit(muxing_params)
                self.wait = True

            else:
                QThread.msleep(50)
                # print("LOG :"+str(self.wait))
        self.all_finished.emit()
