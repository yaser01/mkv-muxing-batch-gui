import subprocess
import traceback

from PySide2.QtCore import Signal, QObject, QThread

from packages.Startup import GlobalFiles
from packages.Tabs.GlobalSetting import write_to_log_file


class StartMuxingProcessWorker(QObject):
    finished_job_signal = Signal(int)
    all_finished = Signal()

    def __init__(self, command=""):
        super().__init__()
        self.command = command
        self.wait = True
        self.stop = False

    def run(self):
        try:
            while not self.stop:
                if not self.wait:
                    with open(GlobalFiles.MuxingLogFilePath, "a+", encoding="UTF-8") as log_file:
                        mux_process = subprocess.run(self.command, shell=True, stdout=log_file, env=GlobalFiles.ENVIRONMENT)
                    self.finished_job_signal.emit(mux_process.returncode)
                    self.wait = True
                else:
                    QThread.msleep(50)
            self.all_finished.emit()
        except Exception as e:
            write_to_log_file(traceback.format_exc())
