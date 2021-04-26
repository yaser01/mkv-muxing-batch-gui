import time

from PySide2.QtCore import QObject, QThread, Signal

from packages.Startup import GlobalFiles
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.MuxSetting.Widgets.GetJsonForMkvmergeJob import GetJsonForMkvmergeJob
from packages.Tabs.MuxSetting.Widgets.GetJsonForMkvpropeditJob import GetJsonForMkvpropeditJob
from packages.Tabs.MuxSetting.Widgets.MuxingParams import MuxingParams
from packages.Tabs.MuxSetting.Widgets.ReadFromMkvmergeLogWorker import ReadFromMkvmergeLogWorker
from packages.Tabs.MuxSetting.Widgets.ReadFromMkvpropeditLogWorker import ReadFromMkvpropeditLogWorker
from packages.Tabs.MuxSetting.Widgets.SingleJobData import SingleJobData
from packages.Tabs.MuxSetting.Widgets.StartMuxingProcessWorker import StartMuxingProcessWorker


def check_if_mkvpropedit_good():
    if len(
            GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST) > 0 or GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_ENABLED == True or GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_ENABLED == True or not GlobalSetting.VIDEO_SOURCE_MKV_ONLY:
        return False
    else:
        return True


def get_time():
    t = time.time()
    return str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)))


def add_double_quotation(string):
    return "\"" + str(string) + "\""


class StartMuxingWorker(QObject):
    finished_all_jobs_signal = Signal()
    finished_paused_signal = Signal()
    cancel_signal = Signal()
    mkvpropedit_good_signal = Signal()
    progress_signal = Signal(MuxingParams)
    job_succeeded_signal = Signal(int)
    job_failed_signal = Signal(int)
    job_started_signal = Signal(int)
    pause_from_error_occurred_signal = Signal()

    def __init__(self, data):
        super().__init__()
        self.data = data  # type:list[SingleJobData]
        self.current_job = -1
        self.finished_read_log_and_muxing = 0
        self.waiting_for_mkvpropedit_confirm = False
        self.always_use_mkvpropedit = False
        self.always_use_mkvmerge = False
        self.use_mkvpropedit = False
        self.use_mkvmerge = False
        self.pause = False
        self.cancel = False
        self.setup_start_muxing_process_thread()
        self.setup_read_mkvmerge_log_thread()
        self.setup_read_mkvpropedit_log_thread()
        self.start_muxing_process_thread.start()
        self.read_log_mkvmerge_thread.start()
        self.read_log_mkvpropedit_thread.start()

    def run(self):
        if self.current_job == len(self.data):
            self.stop_all_threads()
            self.finished_all_jobs_signal.emit()
        self.next_job()

    def stop_all_threads(self):
        self.read_log_mkvmerge_worker.stop = True
        self.read_log_mkvpropedit_worker.stop = True
        self.start_muxing_process_worker.stop = True

    def next_job(self):
        if self.cancel:
            self.stop_all_threads()
            self.cancel_signal.emit()
            return
        self.current_job += 1
        if self.current_job == len(self.data):
            self.stop_all_threads()
            self.finished_all_jobs_signal.emit()
            return
        if self.pause:
            self.stop_all_threads()
            self.finished_paused_signal.emit()
            return

        job = self.data[self.current_job]
        if not job.done:
            GetJsonForMkvmergeJob(job)
            if GlobalSetting.VIDEO_SOURCE_MKV_ONLY:
                GetJsonForMkvpropeditJob(job)
            else:
                self.always_use_mkvmerge = True
            if self.always_use_mkvpropedit:
                self.job_started_signal.emit(self.current_job)
                self.start_mkvpropedit_muxing()
            elif self.always_use_mkvmerge:
                self.job_started_signal.emit(self.current_job)
                self.start_mkvmerge_muxing()
            else:
                if check_if_mkvpropedit_good():
                    self.mkvpropedit_good_signal.emit()
                    self.waiting_for_mkvpropedit_confirm = True
                    while self.waiting_for_mkvpropedit_confirm:
                        time.sleep(0.05)
                    if self.use_mkvpropedit:
                        self.always_use_mkvpropedit = True
                        self.job_started_signal.emit(self.current_job)
                        self.start_mkvpropedit_muxing()
                    elif self.use_mkvmerge:
                        self.always_use_mkvmerge = True
                        self.job_started_signal.emit(self.current_job)
                        self.start_mkvmerge_muxing()
                    else:
                        self.stop_all_threads()
                        self.cancel_signal.emit()
                else:
                    self.always_use_mkvmerge = True
                    self.job_started_signal.emit(self.current_job)
                    self.start_mkvmerge_muxing()
        else:
            self.next_job()

    # noinspection PyAttributeOutsideInit
    def start_mkvpropedit_muxing(self):
        self.data[self.current_job].used_mkvpropedit = True
        mux_command = add_double_quotation(GlobalFiles.MKVPROPEDIT_PATH) + " @" + add_double_quotation(
            GlobalFiles.mkvpropeditJsonJobFilePath)
        self.add_header_info_to_log_file()
        self.start_muxing_process_worker.command = mux_command
        GlobalSetting.MUXING_ON = True
        self.read_log_mkvpropedit_worker.job_index = self.current_job
        self.start_muxing_process_worker.wait = False
        self.read_log_mkvpropedit_worker.wait = False

    def start_mkvmerge_muxing(self):
        mux_command = add_double_quotation(GlobalFiles.MKVMERGE_PATH) + " @" + add_double_quotation(
            GlobalFiles.mkvmergeJsonJobFilePath)
        self.add_header_info_to_log_file()
        self.start_muxing_process_worker.command = mux_command
        GlobalSetting.MUXING_ON = True
        self.read_log_mkvmerge_worker.job_index = self.current_job
        self.start_muxing_process_worker.wait = False
        self.read_log_mkvmerge_worker.wait = False

    # noinspection PyAttributeOutsideInit
    def setup_start_muxing_process_thread(self):
        self.start_muxing_process_worker = StartMuxingProcessWorker()
        self.start_muxing_process_thread = QThread()
        self.start_muxing_process_worker.moveToThread(self.start_muxing_process_thread)
        self.start_muxing_process_thread.started.connect(self.start_muxing_process_worker.run)
        self.start_muxing_process_worker.all_finished.connect(self.start_muxing_process_thread.quit)
        self.start_muxing_process_worker.all_finished.connect(self.start_muxing_process_worker.deleteLater)
        self.start_muxing_process_worker.finished_job_signal.connect(self.finished_muxing_process)

    # noinspection PyAttributeOutsideInit
    def setup_read_mkvmerge_log_thread(self):
        self.read_log_mkvmerge_worker = ReadFromMkvmergeLogWorker(self.current_job)
        self.read_log_mkvmerge_thread = QThread()
        self.read_log_mkvmerge_worker.moveToThread(self.read_log_mkvmerge_thread)
        self.read_log_mkvmerge_thread.started.connect(self.read_log_mkvmerge_worker.run)
        self.read_log_mkvmerge_worker.all_finished.connect(self.read_log_mkvmerge_thread.quit)
        self.read_log_mkvmerge_worker.all_finished.connect(self.read_log_mkvmerge_worker.deleteLater)
        self.read_log_mkvmerge_worker.finished_job_signal.connect(self.finished_read_log)
        self.read_log_mkvmerge_thread.finished.connect(self.read_log_mkvmerge_thread.deleteLater)
        self.read_log_mkvmerge_worker.send_muxing_progress_data_signal.connect(self.receive_muxing_progress_data)

    # noinspection PyAttributeOutsideInit
    def setup_read_mkvpropedit_log_thread(self):
        self.read_log_mkvpropedit_worker = ReadFromMkvpropeditLogWorker(self.current_job)
        self.read_log_mkvpropedit_thread = QThread()
        self.read_log_mkvpropedit_worker.moveToThread(self.read_log_mkvpropedit_thread)
        self.read_log_mkvpropedit_thread.started.connect(self.read_log_mkvpropedit_worker.run)
        self.read_log_mkvpropedit_worker.all_finished.connect(self.read_log_mkvpropedit_thread.quit)
        self.read_log_mkvpropedit_worker.all_finished.connect(self.read_log_mkvpropedit_worker.deleteLater)
        self.read_log_mkvpropedit_worker.finished_job_signal.connect(self.finished_read_log)
        self.read_log_mkvpropedit_thread.finished.connect(self.read_log_mkvpropedit_thread.deleteLater)
        self.read_log_mkvpropedit_worker.send_muxing_progress_data_signal.connect(self.receive_muxing_progress_data)

    def receive_muxing_progress_data(self, params: MuxingParams):
        if params.error:
            if GlobalSetting.MUX_SETTING_ABORT_ON_ERRORS:
                self.pause = True
                self.pause_from_error_occurred_signal.emit()
        self.progress_signal.emit(params)

    def finished_read_log(self):
        self.finished_read_log_and_muxing += 1
        if self.finished_read_log_and_muxing == 2:  # both threads end
            self.add_footer_info_to_log_file()
            GlobalSetting.MUXING_ON = False
            self.finished_read_log_and_muxing = 0
            self.next_job()

    def finished_muxing_process(self, exit_code):
        if exit_code == 2:
            self.job_failed_signal.emit(self.current_job)
            if GlobalSetting.MUX_SETTING_ABORT_ON_ERRORS:
                self.pause = True
        else:
            if self.data[self.current_job].error_occurred:
                self.job_failed_signal.emit(self.current_job)
                if GlobalSetting.MUX_SETTING_ABORT_ON_ERRORS:
                    self.pause = True
            else:
                self.job_succeeded_signal.emit(self.current_job)
        self.finished_read_log_and_muxing += 1
        if self.finished_read_log_and_muxing == 2:  # both threads end
            self.add_footer_info_to_log_file()
            GlobalSetting.MUXING_ON = False
            self.finished_read_log_and_muxing = 0
            self.next_job()

    def add_header_info_to_log_file(self):

        with open(GlobalFiles.LogFilePath, "a+", encoding="UTF-8") as log_file:
            t = get_time()
            log_file.write(
                "\n[" + t + "] Start Muxing: ********* " + str(
                    self.data[self.current_job].video_name) + " *********\n\n")

    def add_footer_info_to_log_file(self):
        with open(GlobalFiles.LogFilePath, "a+", encoding="UTF-8") as log_file:
            t = get_time()
            log_file.write(
                "\n[" + t + "] Finish Muxing: ********* " + self.data[self.current_job].video_name + " *********\n")
