from PySide2.QtCore import Signal
from PySide2.QtWidgets import QGridLayout, QLabel

from packages.Tabs.MuxSetting.Widgets.CompletedJobsCounter import CompletedJobsCounter
from packages.Tabs.MuxSetting.Widgets.JobDividingLine import JobDividingLine
from packages.Tabs.MuxSetting.Widgets.JobQueueTable import JobQueueTable
from packages.Tabs.MuxSetting.Widgets.ProgreeBar import ProgressBar


class JobQueueLayout(QGridLayout):
    update_task_bar_progress_signal = Signal(int)
    paused_done_signal = Signal()
    cancel_done_signal = Signal()
    finished_all_jobs_signal = Signal()
    pause_from_error_occurred_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.table = JobQueueTable()
        self.total_progress_label = QLabel("Total Progress:")
        self.total_progress_progressBar = ProgressBar(value=0, show_percentage=True)
        self.job_dividing_line = JobDividingLine()
        self.completed_jobs_counter = CompletedJobsCounter()
        self.setup_layout()
        self.table.update_total_progress_signal.connect(self.update_total_progress)
        self.table.paused_done_signal.connect(self.paused_done)
        self.table.cancel_done_signal.connect(self.cancel_done)
        self.table.pause_from_error_occurred_signal.connect(self.pause_from_error_occurred)
        self.table.finished_all_jobs_signal.connect(self.finished_all_jobs)
        self.table.increase_number_of_done_jobs_signal.connect(
            self.increase_completed_jobs)
        self.table.set_number_of_jobs_signal.connect(self.set_number_of_jobs)

    def setup_layout(self):
        self.addWidget(self.table, 0, 0, 1, -1)
        self.addWidget(self.total_progress_label, 1, 0, 1, 1)
        self.addWidget(self.total_progress_progressBar, 1, 1, 1, 1)
        self.addWidget(self.job_dividing_line, 1, 2, 1, 1)
        self.addWidget(self.completed_jobs_counter, 1, 3, 1, 1)

    def update_layout(self):
        self.table.update_widget()

    def setup_queue(self):
        self.table.setup_queue()

    def show_necessary_table_columns(self):
        self.table.show_necessary_columns()

    def clear_queue(self):
        self.completed_jobs_counter.initiate_number_of_jobs(0)
        self.total_progress_progressBar.setValue(0)
        self.table.clear_queue()

    def start_muxing(self):
        self.table.start_muxing()

    def paused_done(self):
        self.paused_done_signal.emit()

    def cancel_done(self):
        self.cancel_done_signal.emit()

    def update_total_progress(self, new_progress):
        self.total_progress_progressBar.setValue(new_progress)
        self.update_task_bar_progress_signal.emit(new_progress)

    def increase_completed_jobs(self):
        self.completed_jobs_counter.increase_completed_jobs()

    def set_number_of_jobs(self, number_of_jobs):
        self.completed_jobs_counter.initiate_number_of_jobs(number_of_jobs)

    def pause_muxing(self):
        self.table.pause_muxing()

    def finished_all_jobs(self):
        self.finished_all_jobs_signal.emit()

    def pause_from_error_occurred(self):
        self.pause_from_error_occurred_signal.emit()
