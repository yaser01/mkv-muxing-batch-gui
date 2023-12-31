import os
import time
import traceback
from pathlib import Path

from PySide2.QtCore import QObject, QThread, Signal

from packages.Startup import GlobalFiles
from packages.Tabs.GlobalSetting import GlobalSetting, write_to_log_file
from packages.Tabs.MuxSetting.Widgets.CRCData import CRCData
from packages.Tabs.MuxSetting.Widgets.CalculateCRCProcessWorker import CalculateCRCProcessWorker
from packages.Tabs.MuxSetting.Widgets.GetJsonForMkvmergeJob import GetJsonForMkvmergeJob
from packages.Tabs.MuxSetting.Widgets.GetJsonForMkvpropeditJob import GetJsonForMkvpropeditJob
from packages.Tabs.MuxSetting.Widgets.MuxingParams import MuxingParams
from packages.Tabs.MuxSetting.Widgets.ReadFromMkvmergeLogWorker import ReadFromMkvmergeLogWorker
from packages.Tabs.MuxSetting.Widgets.ReadFromMkvpropeditLogWorker import ReadFromMkvpropeditLogWorker
from packages.Tabs.MuxSetting.Widgets.SingleJobData import SingleJobData
from packages.Tabs.MuxSetting.Widgets.StartMuxingProcessWorker import StartMuxingProcessWorker


def change_file_extension_to_mkv(file_name):
    file_extension_start_index = file_name.rfind(".")
    new_file_name_with_mkv_extension = file_name[:file_extension_start_index] + ".mkv"
    return new_file_name_with_mkv_extension


def check_if_mkvpropedit_good():
    for i in range(len(GlobalSetting.SUBTITLE_FILES_LIST)):
        if len(GlobalSetting.SUBTITLE_FILES_LIST[i]) > 0:
            return False
    for i in range(len(GlobalSetting.AUDIO_FILES_LIST)):
        if len(GlobalSetting.AUDIO_FILES_LIST[i]) > 0:
            return False
    if GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_ENABLED or \
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_ENABLED or \
            (not GlobalSetting.VIDEO_SOURCE_MKV_ONLY) or \
            GlobalSetting.VIDEO_DEFAULT_DURATION_FPS not in ["", "Default"] or \
            GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_REORDER_ACTIVATED or \
            GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_DELETED_ACTIVATED or \
            GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_REORDER_ACTIVATED or \
            GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_DELETED_ACTIVATED or \
            GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_REORDER_ACTIVATED or \
            GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_DELETED_ACTIVATED:
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
    crc_progress_signal = Signal(int)
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
        self.setup_calculate_crc_thread()
        self.start_muxing_process_thread.start()
        self.read_log_mkvmerge_thread.start()
        self.read_log_mkvpropedit_thread.start()
        self.start_crc_calculating_process_thread.start()

    def run(self):
        try:
            if self.current_job == len(self.data):
                self.stop_all_threads()
                self.finished_all_jobs_signal.emit()
            self.next_job()
        except Exception as e:
            write_to_log_file(traceback.format_exc())

    def stop_all_threads(self):
        self.read_log_mkvmerge_worker.stop = True
        self.read_log_mkvpropedit_worker.stop = True
        self.start_muxing_process_worker.stop = True
        self.start_crc_calculating_process_worker.stop = True

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
        if not job.done or (job.error_occurred and job.muxing_message.find("There is not enough space") != -1):
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
                if GlobalSetting.USE_MKVPROPEDIT:
                    self.always_use_mkvpropedit = True
                    self.job_started_signal.emit(self.current_job)
                    self.start_mkvpropedit_muxing()
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

    def check_if_crc_calculating_needed(self):
        if self.data[self.current_job].is_crc_calculating_required:
            if self.data[self.current_job].used_mkvpropedit or GlobalSetting.OVERWRITE_SOURCE_FILES:
                folder_path = os.path.dirname(self.data[self.current_job].video_name_absolute)
            else:
                folder_path = Path(GlobalSetting.DESTINATION_FOLDER_PATH)
            output_file_name = os.path.join(folder_path, self.data[self.current_job].video_name)
            self.start_crc_calculating_process_worker.file_name = output_file_name
            self.start_crc_calculating_process_worker.progress = 0
            self.start_crc_calculating_process_worker.wait = False
            GlobalSetting.MUXING_ON = True
        else:
            GlobalSetting.MUXING_ON = False
            self.next_job()

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
    def setup_calculate_crc_thread(self):
        self.start_crc_calculating_process_worker = CalculateCRCProcessWorker()
        self.start_crc_calculating_process_thread = QThread()
        self.start_crc_calculating_process_worker.moveToThread(self.start_crc_calculating_process_thread)
        self.start_crc_calculating_process_thread.started.connect(self.start_crc_calculating_process_worker.run)
        self.start_crc_calculating_process_worker.all_finished.connect(self.start_crc_calculating_process_thread.quit)
        self.start_crc_calculating_process_worker.all_finished.connect(
            self.start_crc_calculating_process_worker.deleteLater)
        self.start_crc_calculating_process_thread.finished.connect(
            self.start_crc_calculating_process_thread.deleteLater)
        self.start_crc_calculating_process_worker.crc_progress_signal.connect(self.receive_crc_progress)
        self.start_crc_calculating_process_worker.crc_result_signal.connect(self.receive_crc_result)

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

    def receive_crc_progress(self, progress: int):
        self.crc_progress_signal.emit(progress)

    def receive_crc_result(self, crc_string: str):
        crc_data = CRCData()
        crc_data.crc_string = crc_string
        crc_data.job_index = self.current_job
        self.data[self.current_job].new_crc = crc_string
        self.job_succeeded_signal.emit(self.current_job)
        GlobalSetting.MUXING_ON = False
        self.next_job()

    def finished_read_log(self):
        self.finished_read_log_and_muxing += 1
        if self.finished_read_log_and_muxing == 2:  # both threads end
            self.add_footer_info_to_log_file()
            GlobalSetting.MUXING_ON = False
            self.finished_read_log_and_muxing = 0
            if self.data[self.current_job].error_occurred:
                self.next_job()
            else:
                self.check_if_crc_calculating_needed()

    def finished_muxing_process(self, exit_code):
        if exit_code == 2:
            self.data[self.current_job].error_occurred = True
            self.job_failed_signal.emit(self.current_job)
            if GlobalSetting.MUX_SETTING_ABORT_ON_ERRORS:
                self.pause = True
        else:
            if self.data[self.current_job].error_occurred:
                self.job_failed_signal.emit(self.current_job)
                if GlobalSetting.MUX_SETTING_ABORT_ON_ERRORS:
                    self.pause = True
            elif not self.data[self.current_job].is_crc_calculating_required:
                self.job_succeeded_signal.emit(self.current_job)
        self.finished_read_log_and_muxing += 1
        if self.finished_read_log_and_muxing == 2:  # both threads end
            self.add_footer_info_to_log_file()
            GlobalSetting.MUXING_ON = False
            self.finished_read_log_and_muxing = 0
            if self.data[self.current_job].error_occurred:
                self.next_job()
            else:
                self.check_if_crc_calculating_needed()

    def add_header_info_to_log_file(self):

        with open(GlobalFiles.MuxingLogFilePath, "a+", encoding="UTF-8") as log_file:
            t = get_time()
            log_file.write(
                "\n[" + t + "] Start Muxing: ********* " + str(
                    self.data[self.current_job].video_name) + " *********\n\n")

    def add_footer_info_to_log_file(self):
        with open(GlobalFiles.MuxingLogFilePath, "a+", encoding="UTF-8") as log_file:
            t = get_time()
            log_file.write(
                "\n[" + t + "] Finish Muxing: ********* " + self.data[self.current_job].video_name + " *********\n")
