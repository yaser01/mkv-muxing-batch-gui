import subprocess

from PySide2.QtCore import Signal, QObject, QThread

from packages.Startup import GlobalFiles


class StartMuxingProcessWorker(QObject):
    finished_job_signal = Signal(int)
    all_finished = Signal()

    def __init__(self, command=""):
        super().__init__()
        self.command = command
        self.wait = True
        self.stop = False

    def run(self):
        while not self.stop:
            if not self.wait:
                with open(GlobalFiles.LogFilePath, "a+") as log_file:
                    mux_process = subprocess.run(self.command, shell=True, stdout=log_file)
                self.finished_job_signal.emit(mux_process.returncode)
                self.wait = True
            else:
                QThread.msleep(50)
        self.all_finished.emit()
