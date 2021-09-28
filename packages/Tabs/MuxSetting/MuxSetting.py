import os
import time
from os import makedirs
from pathlib import Path
from shutil import copy2

from PySide2.QtCore import Signal
from PySide2.QtGui import QPaintEvent, QResizeEvent
from PySide2.QtWidgets import (
    QVBoxLayout,
    QGroupBox,
    QFileDialog, QCheckBox, QLineEdit, QSizePolicy, QWidget, )

from packages.Tabs.GlobalSetting import GlobalSetting, get_file_name_absolute_path, write_to_log_file
from packages.Tabs.MuxSetting.Widgets.AudioTracksCheckableComboBox import AudioTracksCheckableComboBox
from packages.Tabs.MuxSetting.Widgets.ControlQueueButton import ControlQueueButton
from packages.Tabs.MuxSetting.Widgets.JobQueueLayout import JobQueueLayout
from packages.Tabs.MuxSetting.Widgets.MakeThisAudioDefaultCheckBox import MakeThisAudioDefaultCheckBox
from packages.Tabs.MuxSetting.Widgets.MakeThisSubtitleDefaultCheckBox import MakeThisSubtitleDefaultCheckBox
from packages.Tabs.MuxSetting.Widgets.MakeThisTrackDefaultComboBox import MakeThisTrackDefaultComboBox
from packages.Tabs.MuxSetting.Widgets.OnlyKeepThoseAudiosCheckBox import OnlyKeepThoseAudiosCheckBox
from packages.Tabs.MuxSetting.Widgets.OnlyKeepThoseSubtitlesCheckBox import OnlyKeepThoseSubtitlesCheckBox
from packages.Tabs.MuxSetting.Widgets.SubtitleTracksCheckableComboBox import SubtitleTracksCheckableComboBox
from packages.Widgets.ErrorDialog import ErrorDialog
from packages.Widgets.InfoDialog import InfoDialog
from packages.Widgets.InvalidPathDialog import *


# noinspection PyAttributeOutsideInit


def get_time():
    t = time.time()
    return str(time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(t)))


def change_global_LogFilePath():
    t = get_time()
    log_file_name = "muxing_log_file_" + t + ".txt"
    GlobalFiles.MuxingLogFilePath = get_file_name_absolute_path(file_name=log_file_name,
                                                                folder_path=GlobalFiles.MergeLogsFolderPath)


def check_is_there_subtitle_to_mux():
    for i in GlobalSetting.SUBTITLE_FILES_LIST.keys():
        if len(GlobalSetting.SUBTITLE_FILES_LIST[i]) > 0:
            return True
    return False


# noinspection PyAttributeOutsideInit
def check_if_at_least_one_muxing_setting_has_been_selected():
    if check_is_there_subtitle_to_mux or \
            len(GlobalSetting.ATTACHMENT_FILES_LIST) > 0 or \
            len(GlobalSetting.CHAPTER_FILES_LIST) > 0 or \
            GlobalSetting.ATTACHMENT_DISCARD_OLD or \
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_ENABLED or \
            GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_ENABLED or \
            GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_TRACK != "" or \
            GlobalSetting.MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_TRACK != "":
        return True
    else:
        no_setting_to_apply_dialog = InfoDialog(window_title="No Setting Selected",
                                                info_message="You haven't select any "
                                                             "setting to apply")
        no_setting_to_apply_dialog.execute()
        return False


def check_if_want_to_keep_log_file():
    if GlobalSetting.MUX_SETTING_KEEP_LOG_FILE:
        try:
            copy2(GlobalFiles.MuxingLogFilePath, GlobalSetting.DESTINATION_FOLDER_PATH)
        except Exception as e:
            write_to_log_file(e)
            error_dialog = ErrorDialog(window_title="Permission Denied",
                                       info_message="Can't save log file, MKV Muxing Batch GUI lacks write "
                                                    "permissions on Destination folder")
            error_dialog.execute()


class MuxSettingTab(QWidget):
    tab_clicked_signal = Signal()
    start_muxing_signal = Signal()
    update_task_bar_progress_signal = Signal(int)
    update_task_bar_paused_signal = Signal()
    update_task_bar_clear_signal = Signal()

    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.setup_widgets()
        self.connect_signals()

    def connect_signals(self):
        self.tab_clicked_signal.connect(self.tab_clicked)

        self.destination_path_button.clicked.connect(self.open_select_destination_folder_dialog)

        self.only_keep_those_audios_checkBox.stateChanged.connect(
            self.only_keep_those_audios_multi_choose_comboBox.check_box_state_changed)

        self.only_keep_those_subtitles_checkBox.stateChanged.connect(
            self.only_keep_those_subtitles_multi_choose_comboBox.check_box_state_changed)

        self.make_this_audio_default_checkBox.disable_combo_box.connect(self.disable_make_this_audio_default_comboBox)

        self.make_this_subtitle_default_checkBox.disable_combo_box.connect(
            self.disable_make_this_subtitle_default_comboBox)

        self.control_queue_button.add_to_queue_clicked_signal.connect(self.add_to_queue_button_clicked)
        self.control_queue_button.start_multiplexing_clicked_signal.connect(self.start_multiplexing_button_clicked)
        self.control_queue_button.pause_multiplexing_clicked_signal.connect(self.pause_multiplexing_button_clicked)

        self.clear_job_queue_button.clicked.connect(self.clear_job_queue_button_clicked)

        self.only_keep_those_audios_multi_choose_comboBox.closeList.connect(self.only_keep_those_audios_close_list)

        self.only_keep_those_subtitles_multi_choose_comboBox.closeList.connect(
            self.only_keep_those_subtitles_close_list)

        self.make_this_audio_default_comboBox.currentTextChanged.connect(
            self.make_this_audio_default_comboBox_text_changed)

        self.make_this_subtitle_default_comboBox.currentTextChanged.connect(
            self.make_this_subtitle_default_comboBox_text_changed)

        self.abort_on_errors_checkBox.stateChanged.connect(self.abort_on_errors_state_changed)

        self.keep_log_file_checkBox.stateChanged.connect(self.keep_log_file_state_changed)
        self.job_queue_layout.update_task_bar_progress_signal.connect(self.update_task_bar_progress)
        self.job_queue_layout.paused_done_signal.connect(self.paused_done)
        self.job_queue_layout.cancel_done_signal.connect(self.cancel_done)
        self.job_queue_layout.finished_all_jobs_signal.connect(self.finished_all_jobs)
        self.job_queue_layout.pause_from_error_occurred_signal.connect(self.pause_multiplexing_button_clicked)

    def setup_widgets(self):
        self.setup_mux_setting_groupBox()
        self.setup_job_queue_groupBox()
        self.setup_destination_path_label()
        self.setup_destination_path_lineEdit()
        self.setup_destination_path_button()
        self.setup_abort_on_errors_checkBox()
        self.setup_discard_old_attachments_checkBox()
        self.setup_keep_log_file_checkBox()
        self.setup_clear_job_queue_button()
        self.setup_tool_tip_hint()
        self.setup_layouts()

    def setup_layouts(self):
        self.setup_MainLayout()
        self.mux_setting_groupBox.setLayout(self.mux_setting_layout)
        self.job_queue_groupBox.setLayout(self.job_queue_layout)
        self.setup_mux_tools_layout_first_row()
        self.setup_mux_tools_layout_second_row()
        self.setup_mux_setting_layout()
        self.setLayout(self.MainLayout)

    # noinspection PyAttributeOutsideInit
    def create_widgets(self):
        self.MainLayout = QVBoxLayout()
        self.mux_setting_groupBox = QGroupBox(self)
        self.job_queue_groupBox = QGroupBox(self)
        self.mux_setting_layout = QGridLayout()
        self.job_queue_layout = JobQueueLayout()
        self.destination_path_label = QLabel()
        self.destination_path_lineEdit = QLineEdit()
        self.destination_path_button = QPushButton()
        self.only_keep_those_audios_checkBox = OnlyKeepThoseAudiosCheckBox()
        self.only_keep_those_subtitles_checkBox = OnlyKeepThoseSubtitlesCheckBox()
        self.only_keep_those_audios_multi_choose_comboBox = AudioTracksCheckableComboBox()
        self.only_keep_those_subtitles_multi_choose_comboBox = SubtitleTracksCheckableComboBox()
        self.make_this_audio_default_checkBox = MakeThisAudioDefaultCheckBox()
        self.make_this_subtitle_default_checkBox = MakeThisSubtitleDefaultCheckBox()
        self.make_this_audio_default_comboBox = MakeThisTrackDefaultComboBox()
        self.make_this_subtitle_default_comboBox = MakeThisTrackDefaultComboBox()
        self.abort_on_errors_checkBox = QCheckBox()
        self.discard_old_attachments_checkBox = QCheckBox()
        self.keep_log_file_checkBox = QCheckBox()
        self.control_queue_button = ControlQueueButton()
        self.clear_job_queue_button = QPushButton()
        self.mux_tools_layout_first_row = QHBoxLayout()
        self.mux_tools_layout_second_row = QHBoxLayout()
        self.job_queue_tools_layout = QHBoxLayout()

    def setup_mux_setting_layout(self):
        self.mux_setting_layout.addWidget(self.destination_path_label, 0, 0)
        self.mux_setting_layout.addWidget(self.destination_path_lineEdit, 0, 1)
        self.mux_setting_layout.addWidget(self.destination_path_button, 0, 2)
        self.mux_setting_layout.addWidget(self.only_keep_those_audios_checkBox, 1, 0)
        self.mux_setting_layout.addWidget(self.only_keep_those_subtitles_checkBox, 2, 0)
        self.mux_setting_layout.addLayout(self.mux_tools_layout_first_row, 1, 1)
        self.mux_setting_layout.addLayout(self.mux_tools_layout_second_row, 2, 1)

    def setup_mux_tools_layout_first_row(self):
        self.mux_tools_layout_first_row.addWidget(self.only_keep_those_audios_multi_choose_comboBox, 2)
        self.mux_tools_layout_first_row.addWidget(self.make_this_audio_default_checkBox, 1)
        self.mux_tools_layout_first_row.addWidget(self.make_this_audio_default_comboBox, 2)
        self.mux_tools_layout_first_row.addWidget(self.abort_on_errors_checkBox, 1)
        self.mux_tools_layout_first_row.addWidget(self.keep_log_file_checkBox)

    def setup_mux_tools_layout_second_row(self):
        self.mux_tools_layout_second_row.addWidget(self.only_keep_those_subtitles_multi_choose_comboBox, 2)
        self.mux_tools_layout_second_row.addWidget(self.make_this_subtitle_default_checkBox, 1)
        self.mux_tools_layout_second_row.addWidget(self.make_this_subtitle_default_comboBox, 2)
        self.mux_tools_layout_second_row.addWidget(self.control_queue_button, 1)
        self.mux_tools_layout_second_row.addWidget(self.clear_job_queue_button, 1)

    def setup_clear_job_queue_button(self):
        self.clear_job_queue_button.setText("Clear All")
        self.clear_job_queue_button.setIcon(GlobalFiles.CleanIcon)
        self.clear_job_queue_button.setDisabled(True)

    def setup_keep_log_file_checkBox(self):
        self.keep_log_file_checkBox.setText("Keep Log File")
        self.keep_log_file_checkBox.setToolTip("log file will located in the source folder after finished muxing")

    def setup_discard_old_attachments_checkBox(self):
        self.discard_old_attachments_checkBox.setText("Discard Old Attachments ")

    def setup_abort_on_errors_checkBox(self):
        self.abort_on_errors_checkBox.setText("Abort On Errors")
        self.abort_on_errors_checkBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

    def setup_destination_path_button(self):
        self.destination_path_button.setIcon(GlobalFiles.SelectFolderIcon)

    def setup_destination_path_lineEdit(self):
        self.destination_path_lineEdit.setPlaceholderText("Enter Destination Folder Path")
        self.destination_path_lineEdit.setClearButtonEnabled(True)

    def setup_destination_path_label(self):
        self.destination_path_label.setText("Videos Destination Folder :")

    def setup_MainLayout(self):
        self.MainLayout.addWidget(self.mux_setting_groupBox)
        self.MainLayout.addWidget(self.job_queue_groupBox)

    def setup_job_queue_groupBox(self):
        self.job_queue_groupBox.setTitle("Job Queue")

    def setup_mux_setting_groupBox(self):
        self.mux_setting_groupBox.setTitle("Mux Setting")

    def paintEvent(self, event: QPaintEvent):
        self.update_widgets_size()
        super().paintEvent(event)

    def resizeEvent(self, event: QResizeEvent):
        self.job_queue_layout.update_layout()
        super().resizeEvent(event)

    def update_widgets_size(self):
        self.only_keep_those_subtitles_multi_choose_comboBox.resize(
            self.only_keep_those_audios_multi_choose_comboBox.width(),
            self.only_keep_those_audios_multi_choose_comboBox.height(),
        )

        self.make_this_subtitle_default_checkBox.resize(
            self.make_this_audio_default_checkBox.width(),
            self.make_this_audio_default_checkBox.height(),
        )
        self.make_this_subtitle_default_checkBox.move(
            self.make_this_audio_default_checkBox.x(),
            self.make_this_subtitle_default_checkBox.y(),
        )

        self.make_this_subtitle_default_comboBox.resize(
            self.make_this_audio_default_comboBox.width(),
            self.make_this_audio_default_comboBox.height(),
        )
        self.make_this_subtitle_default_comboBox.move(
            self.make_this_audio_default_comboBox.x(),
            self.make_this_subtitle_default_comboBox.y(),
        )

        self.control_queue_button.move(
            self.abort_on_errors_checkBox.x(),
            self.control_queue_button.y(),
        )

        self.clear_job_queue_button.move(
            self.control_queue_button.x() + self.control_queue_button.width() + 5,
            self.clear_job_queue_button.y(),
        )

    def open_select_destination_folder_dialog(self):
        temp_folder_path = QFileDialog.getExistingDirectory(self, caption="Choose Destination Folder",
                                                            dir=GlobalSetting.LAST_DIRECTORY_PATH, )
        if temp_folder_path == "" or temp_folder_path.isspace():
            return
        elif Path(temp_folder_path) in GlobalSetting.VIDEO_SOURCE_PATHS:
            invalid_dialog = InvalidPathDialog(
                error_message="Some Source and destination videos are in the same folder")
            invalid_dialog.execute()
            return
        else:
            self.destination_path_lineEdit.setText(str(Path(temp_folder_path)))
            GlobalSetting.LAST_DIRECTORY_PATH = self.destination_path_lineEdit.text()
            GlobalSetting.DESTINATION_FOLDER_PATH = self.destination_path_lineEdit.text()

    def check_destination_path(self):
        temp_destination_path = self.destination_path_lineEdit.text()
        try:
            if temp_destination_path == "" or temp_destination_path.isspace():
                temp_destination_path = "[Empty Path]"
                raise Exception(
                    "[WinError 998] Empty path is Not a valid path : " + temp_destination_path)
            # check if system is windows so path must have # SOME_LETTER:\
            if os.name == 'nt':
                if temp_destination_path[1:3] != ":\\" and self.destination_path_lineEdit.text()[
                                                           1:3] != ":/":
                    raise Exception("[WinError 999] Not a valid path : " + temp_destination_path)
            makedirs(temp_destination_path, exist_ok=True)
            ## test if i can write into this path:
            test_file_name = str(time.time()) + ".txt"
            test_file_name_absolute = os.path.join(Path(temp_destination_path), Path(test_file_name))
            try:
                with open(test_file_name_absolute, 'w+') as test_file:
                    test_file.write("Test")
                os.remove(test_file_name_absolute)
            except Exception as e:
                write_to_log_file(e)
                invaild_dialog = InvalidPathDialog(window_title="Permission Denied",
                                                   error_message="MKV Muxing Batch GUI lacks write "
                                                                 "permissions on Destination folder")
                invaild_dialog.execute()
                self.destination_path_lineEdit.setText(GlobalSetting.DESTINATION_FOLDER_PATH)
                return False
        except Exception as e:
            write_to_log_file(e)
            error_message = ""
            if temp_destination_path == "[Empty Path]":
                error_message = "Enter a valid destination path"
            else:
                error_message = temp_destination_path + "\nisn't a valid path!"
            invalid_dialog = InvalidPathDialog(error_message=error_message)
            invalid_dialog.execute()
            self.destination_path_lineEdit.setText(GlobalSetting.DESTINATION_FOLDER_PATH)
            return False
        if Path(temp_destination_path) in GlobalSetting.VIDEO_SOURCE_PATHS:
            invalid_dialog = InvalidPathDialog(
                error_message="Some Source and destination videos are in the same folder")
            invalid_dialog.execute()
            self.destination_path_lineEdit.setText(GlobalSetting.DESTINATION_FOLDER_PATH)
            return False
        GlobalSetting.DESTINATION_FOLDER_PATH = temp_destination_path
        return True

    def setup_tool_tip_hint(self):
        self.only_keep_those_subtitles_multi_choose_comboBox.set_tool_tip_hint()
        self.only_keep_those_audios_multi_choose_comboBox.set_tool_tip_hint()
        self.make_this_subtitle_default_checkBox.set_tool_tip_hint_no_check()
        self.make_this_audio_default_checkBox.set_tool_tip_hint_no_check()

    def add_to_queue_button_clicked(self):
        self.job_queue_layout.setup_queue()
        self.enable_muxing_setting()
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            self.disable_editable_widgets()
            self.control_queue_button.set_state_start_multiplexing()
            self.clear_job_queue_button.setDisabled(False)
            change_global_LogFilePath()
        else:
            self.enable_editable_widgets()
            self.setup_enable_options_for_mkv_only_options()

    def tab_clicked(self):
        self.job_queue_layout.show_necessary_table_columns()
        self.setup_enable_options_for_mkv_only_options()

    def setup_enable_options_for_mkv_only_options(self):
        if GlobalSetting.JOB_QUEUE_EMPTY:
            if GlobalSetting.VIDEO_SOURCE_MKV_ONLY:
                self.only_keep_those_audios_checkBox.setEnabled(True)
                self.only_keep_those_subtitles_checkBox.setEnabled(True)
                self.make_this_audio_default_checkBox.setEnabled(True)
                self.make_this_subtitle_default_checkBox.setEnabled(True)
                self.only_keep_those_audios_checkBox.setToolTip("")
                self.only_keep_those_subtitles_checkBox.setToolTip("")
                self.make_this_audio_default_comboBox.setToolTip("")
                self.make_this_subtitle_default_comboBox.setToolTip("")
                self.setup_tool_tip_hint()
            else:

                self.only_keep_those_subtitles_checkBox.setCheckState(Qt.Unchecked)
                self.only_keep_those_audios_checkBox.setCheckState(Qt.Unchecked)
                self.make_this_audio_default_checkBox.setCheckState(Qt.Unchecked)
                self.make_this_subtitle_default_checkBox.setCheckState(Qt.Unchecked)

                self.only_keep_those_audios_checkBox.setEnabled(False)
                self.only_keep_those_subtitles_checkBox.setEnabled(False)
                self.make_this_audio_default_checkBox.setEnabled(False)
                self.make_this_subtitle_default_checkBox.setEnabled(False)
                self.only_keep_those_audios_checkBox.setToolTip("<b>[Disabled]</b> Only works when video files "
                                                                "are Mkv only")
                self.only_keep_those_subtitles_checkBox.setToolTip("<b>[Disabled]</b> Only works when video files "
                                                                   "are Mkv only")

                self.make_this_audio_default_checkBox.setToolTip("<b>[Disabled]</b> Only works when video files "
                                                                 "are Mkv only")

                self.make_this_subtitle_default_checkBox.setToolTip("<b>[Disabled]</b> Only works when video files "
                                                                    "are Mkv only")
                self.make_this_audio_default_comboBox.setToolTip("<b>[Disabled]</b> Only works when video files "
                                                                 "are Mkv only")
                self.make_this_subtitle_default_comboBox.setToolTip("<b>[Disabled]</b> Only works when video files "
                                                                    "are Mkv only")
                self.only_keep_those_audios_multi_choose_comboBox.setToolTip(
                    "<b>[Disabled]</b> Only works when video files "
                    "are Mkv only")
                self.only_keep_those_subtitles_multi_choose_comboBox.setToolTip(
                    "<b>[Disabled]</b> Only works when video files "
                    "are Mkv only")

    def clear_job_queue_button_clicked(self):
        self.job_queue_layout.clear_queue()
        self.control_queue_button.set_state_add_to_queue()
        self.clear_job_queue_button.setDisabled(True)
        self.control_queue_button.setDisabled(False)
        self.enable_editable_widgets()
        self.enable_muxing_setting()
        self.setup_enable_options_for_mkv_only_options()
        self.update_task_bar_clear_signal.emit()

    def disable_editable_widgets(self):
        self.only_keep_those_subtitles_checkBox.setEnabled(False)
        self.only_keep_those_subtitles_multi_choose_comboBox.setEnabled(False)
        self.only_keep_those_audios_checkBox.setEnabled(False)
        self.only_keep_those_audios_multi_choose_comboBox.setEnabled(False)
        self.make_this_subtitle_default_checkBox.setEnabled(False)
        self.make_this_subtitle_default_comboBox.setEnabled(False)
        self.make_this_audio_default_checkBox.setEnabled(False)
        self.make_this_audio_default_comboBox.setEnabled(False)

    def enable_editable_widgets(self):
        self.only_keep_those_subtitles_checkBox.setEnabled(True)
        self.only_keep_those_subtitles_multi_choose_comboBox.setEnabled(
            self.only_keep_those_subtitles_checkBox.isChecked())
        self.only_keep_those_audios_checkBox.setEnabled(True)
        self.only_keep_those_audios_multi_choose_comboBox.setEnabled(self.only_keep_those_audios_checkBox.isChecked())
        self.make_this_subtitle_default_checkBox.setEnabled(True)
        self.make_this_subtitle_default_comboBox.setEnabled(self.make_this_subtitle_default_checkBox.isChecked())
        self.make_this_audio_default_checkBox.setEnabled(True)
        self.make_this_audio_default_comboBox.setEnabled(self.make_this_audio_default_checkBox.isChecked())

    def only_keep_those_audios_close_list(self):
        GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_LANGUAGES = self.only_keep_those_audios_multi_choose_comboBox.languages
        GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS = self.only_keep_those_audios_multi_choose_comboBox.tracks

    def only_keep_those_subtitles_close_list(self):
        GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_LANGUAGES = self.only_keep_those_subtitles_multi_choose_comboBox.languages
        GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS = self.only_keep_those_subtitles_multi_choose_comboBox.tracks

    def disable_make_this_subtitle_default_comboBox(self, state):
        self.make_this_subtitle_default_comboBox.setDisabled(state)
        if state:
            self.make_this_subtitle_default_comboBox.setCurrentIndex(-1)

    def disable_make_this_audio_default_comboBox(self, state):
        self.make_this_audio_default_comboBox.setDisabled(state)
        if state:
            self.make_this_audio_default_comboBox.setCurrentIndex(-1)

    def make_this_audio_default_comboBox_text_changed(self):
        GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_TRACK = str(
            self.make_this_audio_default_comboBox.currentText())

    def make_this_subtitle_default_comboBox_text_changed(self):
        GlobalSetting.MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_TRACK = str(
            self.make_this_subtitle_default_comboBox.currentText())

    def update_task_bar_progress(self, new_progress):
        self.update_task_bar_progress_signal.emit(new_progress)

    def enable_muxing_setting(self):
        self.destination_path_lineEdit.setEnabled(True)
        self.destination_path_button.setEnabled(True)
        self.abort_on_errors_checkBox.setEnabled(True)
        self.keep_log_file_checkBox.setEnabled(True)

    def disable_muxing_setting(self):
        self.destination_path_lineEdit.setEnabled(False)
        self.destination_path_button.setEnabled(False)
        self.abort_on_errors_checkBox.setEnabled(False)
        self.keep_log_file_checkBox.setEnabled(False)

    @staticmethod
    def abort_on_errors_state_changed(state):
        GlobalSetting.MUX_SETTING_ABORT_ON_ERRORS = bool(state)

    @staticmethod
    def keep_log_file_state_changed(state):
        GlobalSetting.MUX_SETTING_KEEP_LOG_FILE = bool(state)

    def start_multiplexing_button_clicked(self):
        at_least_one_muxing_setting_has_been_selected = check_if_at_least_one_muxing_setting_has_been_selected()
        if at_least_one_muxing_setting_has_been_selected:
            destination_path_valid = self.check_destination_path()
            if destination_path_valid:
                self.setup_log_file()
                self.control_queue_button.set_state_pause_multiplexing()
                self.disable_muxing_setting()
                self.job_queue_layout.start_muxing()
                self.start_muxing_signal.emit()
                self.clear_job_queue_button.setDisabled(True)

    def pause_multiplexing_button_clicked(self):
        self.job_queue_layout.pause_muxing()
        self.control_queue_button.setDisabled(True)
        self.control_queue_button.set_state_pausing_multiplexing()

    def paused_done(self):
        self.control_queue_button.set_state_resume_multiplexing()
        self.clear_job_queue_button.setDisabled(False)
        self.control_queue_button.setDisabled(False)
        self.update_task_bar_paused_signal.emit()

    def cancel_done(self):
        self.disable_editable_widgets()
        self.enable_muxing_setting()
        self.control_queue_button.set_state_start_multiplexing()
        self.clear_job_queue_button.setDisabled(False)
        change_global_LogFilePath()

    def finished_all_jobs(self):
        self.enable_editable_widgets()
        self.enable_muxing_setting()
        self.setup_enable_options_for_mkv_only_options()
        self.control_queue_button.set_state_start_multiplexing()
        self.control_queue_button.setDisabled(True)
        self.clear_job_queue_button.setDisabled(False)
        self.update_task_bar_clear_signal.emit()
        GlobalSetting.JOB_QUEUE_EMPTY = True
        check_if_want_to_keep_log_file()

    def setup_log_file(self):
        if self.control_queue_button.state == "START":
            open(GlobalFiles.MuxingLogFilePath, 'w+').close()
