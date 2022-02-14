import time

from PySide2.QtCore import Qt, QThread
from PySide2.QtGui import QMovie
from PySide2.QtWidgets import QDialog, QLabel, QHBoxLayout

from packages.Startup.GlobalFiles import SpinnerIconPath
from packages.Tabs.VideoTab.Widgets.GenerateMediaInfoFilesWorker import GenerateMediaInfoFilesWorker


class LoadingVideosInfoDialog(QDialog):
    def __init__(self, videos_list):
        super().__init__()
        self.setWindowTitle("Loading Media Info")
        self.videos_list = videos_list
        self.videos_count = len(self.videos_list)
        self.current_video_done_index = 0
        self.unsupported_files_list = []
        self.status_label = QLabel(
            "Scanning Video " + str(self.current_video_done_index) + "/" + str(self.videos_count))
        self.load_icon_movie = QMovie(SpinnerIconPath)
        self.load_icon_label = QLabel()
        self.load_icon_label.setMovie(self.load_icon_movie)
        self.layout = QHBoxLayout()
        self.layout.addStretch(2)
        self.layout.addWidget(self.load_icon_label)
        self.layout.addWidget(self.status_label)
        self.layout.addStretch(3)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(8, 12, 8, 12)
        self.setLayout(self.layout)
        self.disable_question_mark_window()
        self.generate_media_info_files()

    # noinspection PyAttributeOutsideInit
    def generate_media_info_files(self):
        self.generate_media_info_files_thread = QThread()
        self.generate_media_info_files_worker = GenerateMediaInfoFilesWorker(self.videos_list)
        self.generate_media_info_files_worker.moveToThread(self.generate_media_info_files_thread)
        self.generate_media_info_files_thread.started.connect(self.generate_media_info_files_worker.run)
        self.generate_media_info_files_worker.job_succeeded_signal.connect(self.update_progress)
        self.generate_media_info_files_worker.job_unsupported_file_signal.connect(self.add_new_unsupported_file)
        self.generate_media_info_files_worker.finished_all_jobs_signal.connect(
            self.generate_media_info_files_thread.quit)
        self.generate_media_info_files_worker.finished_all_jobs_signal.connect(
            self.generate_media_info_files_worker.deleteLater)
        self.generate_media_info_files_thread.finished.connect(self.generate_media_info_files_thread.deleteLater)
        self.generate_media_info_files_thread.finished.connect(self.stop_loading)
        self.start_loading()
        self.generate_media_info_files_thread.start()

    def disable_question_mark_window(self):
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)

    def update_progress(self):
        self.current_video_done_index += 1
        self.status_label.setText(
            " Scanning Video " + str(self.current_video_done_index) + "/" + str(self.videos_count))

    def add_new_unsupported_file(self, file_name):
        self.unsupported_files_list.append(file_name)

    def start_loading(self):
        self.load_icon_movie.start()

    def stop_loading(self):
        time.sleep(0.1)
        self.load_icon_movie.stop()

        self.close()

    def execute(self):
        self.exec()
