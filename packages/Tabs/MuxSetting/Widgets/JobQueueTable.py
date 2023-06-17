import os
import time
from pathlib import Path

from PySide2.QtCore import QThread, Signal
from PySide2.QtGui import Qt, QFontMetrics
from PySide2.QtWidgets import QAbstractItemView, QTableWidgetItem, QHeaderView, QLabel

from packages.Startup.DefaultOptions import DefaultOptions
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Tabs.GlobalSetting import GlobalSetting, get_readable_filesize
from packages.Tabs.MuxSetting.Widgets.ConfirmUsingMkvpropedit import ConfirmUsingMkvpropedit
from packages.Tabs.MuxSetting.Widgets.MuxingParams import MuxingParams
from packages.Tabs.MuxSetting.Widgets.ProgreeBar import ProgressBar
from packages.Tabs.MuxSetting.Widgets.SingleJobData import SingleJobData
from packages.Tabs.MuxSetting.Widgets.StartMuxingWorker import StartMuxingWorker
from packages.Tabs.MuxSetting.Widgets.StatusWidget import StatusWidget
from packages.Widgets.AudioInfoDialog import AudioInfoDialog
from packages.Widgets.ChapterInfoDialog import ChapterInfoDialog
from packages.Widgets.ErrorCell import ErrorCell
from packages.Widgets.ErrorMuxingDialog import ErrorMuxingDialog
from packages.Widgets.InfoCell import InfoCell
from packages.Widgets.InfoWithOptionsCell import InfoWithOptionsCell
from packages.Widgets.OkCell import OkCell
from packages.Widgets.OkDialog import OkDialog
from packages.Widgets.SubtitleInfoDialog import SubtitleInfoDialog
from packages.Widgets.TableWidget import TableWidget
from packages.Widgets.WarningCell import WarningCell
from packages.Widgets.WarningDialog import WarningDialog


def generate_tool_tip_for_chapter_file(chapter_full_path="C:/Test", chapter_name="Test", show_full_path=True):
    if show_full_path:
        return (
                "Chapter Full Path: " + str(chapter_full_path) +
                "\nChapter Name: " + str(chapter_name) +
                "\nDouble click for more details")
    else:
        return ("Chapter Name: " + str(chapter_name) +
                "\nDouble click for more details")


def generate_tool_tip_for_audio_file(audio_full_path="C:/Test", audio_name="Test",
                                     audio_delay=0.0, audio_language=DefaultOptions.Default_Audio_Language,
                                     audio_track_name="Test",
                                     audio_set_default=False, audio_set_forced=False,
                                     show_full_path=False):
    if show_full_path:
        return (
                "Audio Full Path: " + str(audio_full_path) +
                "\nAudio Name: " + str(audio_name) +
                "\nAudio Delay: " + str(audio_delay) + "s" +
                "\nAudio Language: " + str(audio_language) +
                "\nAudio Track Name: " + str(audio_track_name) +
                "\nSet Default: " + str(audio_set_default) +
                "\nSet Forced: " + str(audio_set_forced) +
                "\nDouble click for more details")
    else:
        return (
                "Audio Name: " + str(audio_name) +
                "\nAudio Delay: " + str(audio_delay) + "s" +
                "\nAudio Language: " + str(audio_language) +
                "\nAudio Track Name: " + str(audio_track_name) +
                "\nSet Default: " + str(audio_set_default) +
                "\nSet Forced: " + str(audio_set_forced) +
                "\nDouble click for more details")


def generate_tool_tip_for_subtitle_file(subtitle_full_path="C:/Test", subtitle_name="Test",
                                        subtitle_delay=0.0, subtitle_language=DefaultOptions.Default_Subtitle_Language,
                                        subtitle_track_name="Test",
                                        subtitle_set_default=False, subtitle_set_forced=False,
                                        show_full_path=False):
    if show_full_path:
        return (
                "Subtitle Full Path: " + str(subtitle_full_path) +
                "\nSubtitle Name: " + str(subtitle_name) +
                "\nSubtitle Delay: " + str(subtitle_delay) + "s" +
                "\nSubtitle Language: " + str(subtitle_language) +
                "\nSubtitle Track Name: " + str(subtitle_track_name) +
                "\nSet Default: " + str(subtitle_set_default) +
                "\nSet Forced: " + str(subtitle_set_forced) +
                "\nDouble click for more details")
    else:
        return (
                "Subtitle Name: " + str(subtitle_name) +
                "\nSubtitle Delay: " + str(subtitle_delay) + "s" +
                "\nSubtitle Language: " + str(subtitle_language) +
                "\nSubtitle Track Name: " + str(subtitle_track_name) +
                "\nSet Default: " + str(subtitle_set_default) +
                "\nSet Forced: " + str(subtitle_set_forced) +
                "\nDouble click for more details")


def get_file_name_with_mkv_extension(file_name):
    file_extension_start_index = file_name.rfind(".")
    new_file_name_with_mkv_extension = file_name[:file_extension_start_index] + ".mkv"
    return new_file_name_with_mkv_extension


# noinspection PyUnresolvedReferences
def change_file_extension_to_mkv_with_random_suffix(file_name):
    file_extension_start_index = file_name.rfind(".")
    new_file_name_with_mkv_extension = file_name[
                                       :file_extension_start_index] + "#" + GlobalSetting.RANDOM_OUTPUT_SUFFIX + ".mkv "
    return new_file_name_with_mkv_extension


def set_is_job_crc_required(new_job):
    new_job.is_crc_calculating_required = GlobalSetting.MUX_SETTING_ADD_CRC
    new_job.is_crc_removing_required = GlobalSetting.MUX_SETTING_REMOVE_OLD_CRC


def set_attachments_setting_for_job(new_job, new_row_id):
    new_job.discard_old_attachments = GlobalSetting.ATTACHMENT_DISCARD_OLD
    new_job.allow_duplicates_attachments = GlobalSetting.ATTACHMENT_ALLOW_DUPLICATE
    new_job.attachments_absolute_path = []
    if GlobalSetting.ATTACHMENT_EXPERT_MODE:
        if len(GlobalSetting.ATTACHMENT_PATH_DATA_LIST) > new_row_id:
            new_job.attachments_absolute_path = GlobalSetting.ATTACHMENT_PATH_DATA_LIST[new_row_id].files_list.copy()
    else:
        for i in range(len(GlobalSetting.ATTACHMENT_FILES_ABSOLUTE_PATH_LIST)):
            if GlobalSetting.ATTACHMENT_FILES_CHECKING_LIST[i]:
                file_to_attach = GlobalSetting.ATTACHMENT_FILES_ABSOLUTE_PATH_LIST[i]
                new_job.attachments_absolute_path.append(file_to_attach)


Valid_CRC_String = "0123456789ABCDEF"


def get_file_name_without_crc(file_name):
    file_name = str(file_name)
    file_name_without_crc = file_name
    bracket_left_index = file_name.rfind("[")
    bracket_right_index = file_name.rfind("]")
    if (bracket_right_index - bracket_left_index - 1) == 8:
        valid_counter = 0
        for i in range(bracket_left_index + 1, bracket_right_index):
            if file_name[i] in Valid_CRC_String:
                valid_counter += 1
        if valid_counter == 8:
            file_name_without_crc = file_name[:bracket_left_index] + file_name[
                                                                     bracket_right_index + 1:]
    extension_index = file_name_without_crc.rfind(".")
    file_name_without_extension = file_name_without_crc[:extension_index]
    last_valid_char = 0
    for i in range(len(file_name_without_extension) - 1, -1, -1):
        if file_name_without_extension[i] != " ":
            last_valid_char = i
            break
    file_name_without_crc = file_name_without_crc[
                            :last_valid_char + 1] + file_name_without_crc[extension_index:]
    return file_name_without_crc


def get_file_name_with_crc(file_name, crc_string):
    file_name = str(file_name)
    file_name_without_crc = file_name
    bracket_left_index = file_name.rfind("[")
    bracket_right_index = file_name.rfind("]")
    if (bracket_right_index - bracket_left_index - 1) == 8:
        valid_counter = 0
        for i in range(bracket_left_index + 1, bracket_right_index):
            if file_name[i] in Valid_CRC_String:
                valid_counter += 1
        if valid_counter == 8:
            file_name_without_crc = file_name[:bracket_left_index] + file_name[
                                                                     bracket_right_index + 1:]
    extension_index = file_name_without_crc.rfind(".")
    file_name_without_extension = file_name_without_crc[:extension_index]
    last_valid_char = 0
    for i in range(len(file_name_without_extension) - 1, -1, -1):
        if file_name_without_extension[i] != " ":
            last_valid_char = i
            break
    if file_name_without_crc[last_valid_char] in ['[', ']', ')', '(', '}', '{']:
        file_name_with_crc = file_name_without_crc[
                             :last_valid_char + 1] + "[" + crc_string + "]" + file_name_without_crc[
                                                                              extension_index:]
    else:
        file_name_with_crc = file_name_without_crc[
                             :last_valid_char + 1] + " [" + crc_string + "]" + file_name_without_crc[
                                                                               extension_index:]
    return file_name_with_crc


def calculate_size_after_muxing(finished_job: SingleJobData):
    try:
        output_video_size_bytes = os.path.getsize(finished_job.output_video_absolute_path)
    except:
        output_video_size_bytes = 0
    return output_video_size_bytes


def rename_file(file_name_old_crc_absolute_path, file_name_with_crc_absolute_path):
    for i in range(500):
        try:
            os.rename(file_name_old_crc_absolute_path, file_name_with_crc_absolute_path)
            return
        except Exception as e:
            time.sleep(0.05)


class JobQueueTable(TableWidget):
    update_total_progress_signal = Signal(int)
    increase_number_of_done_jobs_signal = Signal()
    set_number_of_jobs_signal = Signal(int)
    paused_done_signal = Signal()
    cancel_done_signal = Signal()
    pause_from_error_occurred_signal = Signal()
    finished_all_jobs_signal = Signal()

    def __init__(self):
        super().__init__()
        self.data = []  # type: list[SingleJobData]
        self.total_progress = 0
        self.number_of_jobs = 0
        self.number_of_done_jobs = 0
        self.need_column_width_set = True
        self.column_ids = {
            "Name": 0,
            "Status": 1,
            "Audio": 2,
            "Subtitle": 3,
            "Chapter": 4,
            "Size Before": 5,
            "Progress": 6,
            "Size After": 7,

        }
        self.setColumnCount(len(self.column_ids))
        self.setRowCount(0)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.create_horizontal_header()
        self.setup_horizontal_header()
        self.setup_columns()
        self.connect_signals()

    def setup_horizontal_header(self):
        self.horizontalHeader().setHighlightSections(False)
        self.horizontal_header.setSectionResizeMode(0, QHeaderView.Interactive)
        self.horizontal_header.setSectionResizeMode(1, QHeaderView.Interactive)
        self.horizontal_header.setSectionResizeMode(2, QHeaderView.Interactive)
        self.horizontal_header.setSectionResizeMode(3, QHeaderView.Interactive)
        self.horizontal_header.setSectionResizeMode(4, QHeaderView.Interactive)
        self.horizontal_header.setSectionResizeMode(5, QHeaderView.Interactive)
        self.horizontal_header.setSectionResizeMode(6, QHeaderView.Interactive)
        self.horizontal_header.setSectionResizeMode(7, QHeaderView.Stretch)

    def create_horizontal_header(self):
        self.horizontal_header = self.horizontalHeader()

    def setup_columns(self):
        column = QTableWidgetItem("Name")
        column.setTextAlignment(Qt.AlignLeft)
        self.setHorizontalHeaderItem(self.column_ids["Name"], column)

        column = QTableWidgetItem("Status")
        column.setTextAlignment(Qt.AlignCenter)
        self.setHorizontalHeaderItem(self.column_ids["Status"], column)

        column = QTableWidgetItem("Audio")
        column.setTextAlignment(Qt.AlignCenter)
        self.setHorizontalHeaderItem(self.column_ids["Audio"], column)

        column = QTableWidgetItem("Subtitle")
        column.setTextAlignment(Qt.AlignCenter)
        self.setHorizontalHeaderItem(self.column_ids["Subtitle"], column)

        column = QTableWidgetItem("Chapter")
        column.setTextAlignment(Qt.AlignCenter)
        self.setHorizontalHeaderItem(self.column_ids["Chapter"], column)

        column = QTableWidgetItem("Size Before")
        column.setTextAlignment(Qt.AlignLeft)
        self.setHorizontalHeaderItem(self.column_ids["Size Before"], column)

        column = QTableWidgetItem("Progress")
        column.setTextAlignment(Qt.AlignLeft)
        self.setHorizontalHeaderItem(self.column_ids["Progress"], column)

        column = QTableWidgetItem("Size After")
        column.setTextAlignment(Qt.AlignLeft)
        self.setHorizontalHeaderItem(self.column_ids["Size After"], column)

    def connect_signals(self):
        self.horizontalHeader().sectionHandleDoubleClicked.connect(
            self.resize_name_column_to_fit_content)
        self.horizontalHeader().sectionResized.connect(self.resize_column)
        self.cellDoubleClicked.connect(self.cell_double_clicked)

    def set_row_value_id(self, new_row_id):
        vertical_header_item = QTableWidgetItem(str(new_row_id + 1))
        vertical_header_item.setTextAlignment(Qt.AlignCenter)
        self.setVerticalHeaderItem(new_row_id, vertical_header_item)

    def set_row_value_size_before_muxing(self, new_job, new_row_id):
        new_job.size_before_muxing = " " + GlobalSetting.VIDEO_FILES_SIZE_LIST[new_row_id]
        self.setCellWidget(new_row_id, self.column_ids["Size Before"], QLabel(new_job.size_before_muxing))

    def set_row_value_size_after_muxing(self, finished_job: SingleJobData, row_index):
        output_video_size_bytes = calculate_size_after_muxing(finished_job)
        if output_video_size_bytes == 0:
            self.delete_video_output_with_zero_size(file_path=finished_job.output_video_absolute_path)
        size_after_muxing = " " + get_readable_filesize(output_video_size_bytes)
        self.setCellWidget(row_index, self.column_ids["Size After"], QLabel(size_after_muxing))

    def set_row_value_chapter(self, new_job, new_row_id):
        if len(GlobalSetting.CHAPTER_FILES_LIST) > new_row_id:
            new_job.chapter_found = True
            new_job.chapter_name = GlobalSetting.CHAPTER_FILES_LIST[new_row_id]
            new_job.chapter_name_absolute = GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[new_row_id]
            self.setCellWidget(new_row_id, self.column_ids["Chapter"],
                               InfoCell(tool_tip=generate_tool_tip_for_chapter_file(
                                   chapter_full_path=new_job.chapter_name_absolute,
                                   chapter_name=new_job.chapter_name,
                                   show_full_path=False)))

        else:
            new_job.chapter_found = False
            self.setCellWidget(new_row_id, self.column_ids["Chapter"],
                               WarningCell(tool_tip="No Chapter File"))

    def set_row_value_subtitle(self, new_job, new_row_id):
        subtitles_count = 0
        for i in GlobalSetting.SUBTITLE_FILES_LIST.keys():
            if len(GlobalSetting.SUBTITLE_FILES_LIST[i]) > new_row_id:
                new_job.subtitle_found = True
                new_job.subtitle_name.append(GlobalSetting.SUBTITLE_FILES_LIST[i][new_row_id])
                new_job.subtitle_name_absolute.append(GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[i][new_row_id])
                new_job.subtitle_delay.append(GlobalSetting.SUBTITLE_DELAY[i])
                new_job.subtitle_language.append(GlobalSetting.SUBTITLE_LANGUAGE[i])
                new_job.subtitle_track_name.append(GlobalSetting.SUBTITLE_TRACK_NAME[i])
                new_job.subtitle_set_default.append(GlobalSetting.SUBTITLE_SET_DEFAULT[i])
                new_job.subtitle_set_forced.append(GlobalSetting.SUBTITLE_SET_FORCED[i])
                new_job.subtitle_set_at_top.append(GlobalSetting.SUBTITLE_SET_ORDER[i])

                subtitles_count += 1
        if subtitles_count == 1:
            new_job.subtitle_found = True
            self.setCellWidget(new_row_id, self.column_ids["Subtitle"],
                               InfoWithOptionsCell(tool_tip=generate_tool_tip_for_subtitle_file(
                                   subtitle_full_path=new_job.subtitle_name_absolute[0],
                                   subtitle_name=new_job.subtitle_name[0],
                                   subtitle_delay=new_job.subtitle_delay[0],
                                   subtitle_language=new_job.subtitle_language[0],
                                   subtitle_track_name=new_job.subtitle_track_name[0],
                                   subtitle_set_default=new_job.subtitle_set_default[0],
                                   subtitle_set_forced=new_job.subtitle_set_forced[0],
                                   show_full_path=False)))
        elif subtitles_count == 0:
            new_job.subtitle_found = False
            self.setCellWidget(new_row_id, self.column_ids["Subtitle"],
                               WarningCell(tool_tip="No Subtitle File"))
        else:
            new_job.subtitle_found = True
            self.setCellWidget(new_row_id, self.column_ids["Subtitle"],
                               InfoWithOptionsCell(tool_tip="Multiple Subtitles\nDouble click for more details"))

    def set_row_value_audio(self, new_job, new_row_id):
        audios_count = 0
        for i in GlobalSetting.AUDIO_FILES_LIST.keys():
            if len(GlobalSetting.AUDIO_FILES_LIST[i]) > new_row_id:
                new_job.audio_found = True
                new_job.audio_name.append(GlobalSetting.AUDIO_FILES_LIST[i][new_row_id])
                new_job.audio_name_absolute.append(GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[i][new_row_id])
                new_job.audio_delay.append(GlobalSetting.AUDIO_DELAY[i])
                new_job.audio_language.append(GlobalSetting.AUDIO_LANGUAGE[i])
                new_job.audio_track_name.append(GlobalSetting.AUDIO_TRACK_NAME[i])
                new_job.audio_set_default.append(GlobalSetting.AUDIO_SET_DEFAULT[i])
                new_job.audio_set_forced.append(GlobalSetting.AUDIO_SET_FORCED[i])
                new_job.audio_set_at_top.append(GlobalSetting.AUDIO_SET_ORDER[i])
                audios_count += 1
        if audios_count == 1:
            new_job.audio_found = True
            self.setCellWidget(new_row_id, self.column_ids["Audio"],
                               InfoWithOptionsCell(tool_tip=generate_tool_tip_for_audio_file(
                                   audio_full_path=new_job.audio_name_absolute[0],
                                   audio_name=new_job.audio_name[0],
                                   audio_delay=new_job.audio_delay[0],
                                   audio_language=new_job.audio_language[0],
                                   audio_track_name=new_job.audio_track_name[0],
                                   audio_set_default=new_job.audio_set_default[0],
                                   audio_set_forced=new_job.audio_set_forced[0],
                                   show_full_path=False)))
        elif audios_count == 0:
            new_job.audio_found = False
            self.setCellWidget(new_row_id, self.column_ids["Audio"],
                               WarningCell(tool_tip="No Audio File"))
        else:
            new_job.audio_found = True
            self.setCellWidget(new_row_id, self.column_ids["Audio"],
                               InfoWithOptionsCell(tool_tip="Multiple Audios\nDouble click for more details"))

    def set_row_value_progressBar(self, new_job, new_row_id):
        new_job.progress = 0
        self.setCellWidget(new_row_id, self.column_ids["Progress"], ProgressBar(value=new_job.progress))

    def set_row_value_name(self, new_job, new_row_id):
        new_job.video_name = GlobalSetting.VIDEO_FILES_LIST[new_row_id]
        new_job.video_name_absolute = GlobalSetting.VIDEO_FILES_ABSOLUTE_PATH_LIST[new_row_id]
        new_job.video_name_with_spaces = " " + new_job.video_name + "   "
        new_job.video_name_displayed = chr(0x200E) + new_job.video_name_with_spaces
        name_label = QLabel(new_job.video_name_displayed)
        name_label.setToolTip(new_job.video_name)
        self.setCellWidget(new_row_id, self.column_ids["Name"], name_label)

    def check_if_name_need_resize_column_to_fit_content(self):
        new_column_width = 0
        for i in range(self.rowCount()):
            column_font = self.cellWidget(i, self.column_ids["Name"]).font()
            column_font_metrics = QFontMetrics(column_font)
            new_column_width = max(new_column_width,
                                   column_font_metrics.horizontalAdvance(self.data[i].video_name_with_spaces))
        if new_column_width > self.columnWidth(self.column_ids["Name"]):
            self.resize_name_column_to_fit_content()

    def resize_name_column_to_fit_content(self):
        # Resize Name Column Only
        new_column_width = 0
        for i in range(self.rowCount()):
            column_font = self.cellWidget(i, self.column_ids["Name"]).font()
            column_font_metrics = QFontMetrics(column_font)
            new_column_width = max(new_column_width,
                                   column_font_metrics.horizontalAdvance(self.data[i].video_name_with_spaces))
        if new_column_width != 0:
            self.setColumnWidth(self.column_ids["Name"], new_column_width)
        for i in range(self.rowCount()):
            self.data[i].video_name_displayed = chr(0x200E) + self.data[i].video_name_with_spaces
            self.cellWidget(i, self.column_ids["Name"]).setText(self.data[i].video_name_displayed)

    def resize_column(self, column_index):
        if column_index == self.column_ids["Name"]:
            for i in range(self.rowCount()):
                metrics = QFontMetrics(
                    self.cellWidget(i, self.column_ids["Name"]).font())
                elided_text = metrics.elidedText(
                    self.data[i].video_name_with_spaces, Qt.ElideRight,
                    self.columnWidth(self.column_ids["Name"]))
                self.data[i].video_name_displayed = chr(0x200E) + elided_text
                self.cellWidget(i, self.column_ids["Name"]).setText(self.data[i].video_name_displayed)
        self.update()

    def cell_double_clicked(self, row_index, column_index):
        if column_index == self.column_ids["Subtitle"]:
            if self.data[row_index].subtitle_found:
                subtitles_default_value_delay_list = []
                subtitles_default_value_language = []
                subtitles_default_value_track_name = []
                subtitles_default_value_set_default = []
                subtitles_default_value_set_forced = []
                for i in GlobalSetting.SUBTITLE_FILES_LIST.keys():
                    if len(GlobalSetting.SUBTITLE_FILES_LIST[i]) > row_index:
                        subtitles_default_value_delay_list.append(GlobalSetting.SUBTITLE_DELAY[i])
                        subtitles_default_value_language.append(GlobalSetting.SUBTITLE_LANGUAGE[i])
                        subtitles_default_value_track_name.append(GlobalSetting.SUBTITLE_TRACK_NAME[i])
                        subtitles_default_value_set_default.append(GlobalSetting.SUBTITLE_SET_DEFAULT[i])
                        subtitles_default_value_set_forced.append(GlobalSetting.SUBTITLE_SET_FORCED[i])
                subtitle_info_dialog = SubtitleInfoDialog(
                    subtitles_name=self.data[row_index].subtitle_name.copy(),
                    subtitles_delay=self.data[row_index].subtitle_delay.copy(),
                    subtitles_language=self.data[row_index].subtitle_language.copy(),
                    subtitles_track_name=self.data[row_index].subtitle_track_name.copy(),
                    subtitles_set_default=self.data[row_index].subtitle_set_default.copy(),
                    subtitles_set_forced=self.data[row_index].subtitle_set_forced.copy(),
                    subtitles_default_value_delay=subtitles_default_value_delay_list,
                    subtitles_default_value_language=subtitles_default_value_language,
                    subtitles_default_value_track_name=subtitles_default_value_track_name,
                    subtitles_default_value_set_default=subtitles_default_value_set_default,
                    subtitles_default_value_set_forced=subtitles_default_value_set_forced,
                    subtitle_set_default_disabled=GlobalSetting.SUBTITLE_SET_DEFAULT_DISABLED,
                    subtitle_set_forced_disabled=GlobalSetting.SUBTITLE_SET_FORCED_DISABLED,
                    disable_edit=GlobalSetting.MUXING_ON,
                )
                subtitle_info_dialog.execute()
                if subtitle_info_dialog.state == "yes":
                    self.data[row_index].subtitle_delay = subtitle_info_dialog.current_subtitle_delay
                    self.data[row_index].subtitle_language = subtitle_info_dialog.current_subtitle_language
                    self.data[row_index].subtitle_track_name = subtitle_info_dialog.current_subtitle_track_name
                    self.data[row_index].subtitle_set_default = subtitle_info_dialog.current_subtitle_set_default
                    self.data[row_index].subtitle_set_forced = subtitle_info_dialog.current_subtitle_set_forced
                    current_cell_widget = self.cellWidget(row_index, self.column_ids["Subtitle"])
                    if len(subtitle_info_dialog.current_subtitle_delay) == 1:
                        current_cell_widget.update_tool_tip(tool_tip=generate_tool_tip_for_subtitle_file(
                            subtitle_full_path=GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[0][row_index],
                            subtitle_name=GlobalSetting.SUBTITLE_FILES_LIST[0][row_index],
                            subtitle_delay=self.data[row_index].subtitle_delay[0],
                            subtitle_language=self.data[row_index].subtitle_language[0],
                            subtitle_track_name=self.data[row_index].subtitle_track_name[0],
                            subtitle_set_default=self.data[row_index].subtitle_set_default[0],
                            subtitle_set_forced=self.data[row_index].subtitle_set_forced[0],
                            show_full_path=False))

            else:
                warning_dialog = WarningDialog(window_title="Subtitle Info", info_message="No subtitle found!")
                warning_dialog.execute()
        elif column_index == self.column_ids["Audio"]:
            if self.data[row_index].audio_found:
                audios_default_value_delay_list = []
                audios_default_value_language = []
                audios_default_value_track_name = []
                audios_default_value_set_default = []
                audios_default_value_set_forced = []
                for i in GlobalSetting.AUDIO_FILES_LIST.keys():
                    if len(GlobalSetting.AUDIO_FILES_LIST[i]) > row_index:
                        audios_default_value_delay_list.append(GlobalSetting.AUDIO_DELAY[i])
                        audios_default_value_language.append(GlobalSetting.AUDIO_LANGUAGE[i])
                        audios_default_value_track_name.append(GlobalSetting.AUDIO_TRACK_NAME[i])
                        audios_default_value_set_default.append(GlobalSetting.AUDIO_SET_DEFAULT[i])
                        audios_default_value_set_forced.append(GlobalSetting.AUDIO_SET_FORCED[i])
                audio_info_dialog = AudioInfoDialog(
                    audios_name=self.data[row_index].audio_name.copy(),
                    audios_delay=self.data[row_index].audio_delay.copy(),
                    audios_language=self.data[row_index].audio_language.copy(),
                    audios_track_name=self.data[row_index].audio_track_name.copy(),
                    audios_set_default=self.data[row_index].audio_set_default.copy(),
                    audios_set_forced=self.data[row_index].audio_set_forced.copy(),
                    audios_default_value_delay=audios_default_value_delay_list,
                    audios_default_value_language=audios_default_value_language,
                    audios_default_value_track_name=audios_default_value_track_name,
                    audios_default_value_set_default=audios_default_value_set_default,
                    audios_default_value_set_forced=audios_default_value_set_forced,
                    audio_set_default_disabled=GlobalSetting.AUDIO_SET_DEFAULT_DISABLED,
                    audio_set_forced_disabled=GlobalSetting.AUDIO_SET_FORCED_DISABLED,
                    disable_edit=GlobalSetting.MUXING_ON,
                )
                audio_info_dialog.execute()
                if audio_info_dialog.state == "yes":
                    self.data[row_index].audio_delay = audio_info_dialog.current_audio_delay
                    self.data[row_index].audio_language = audio_info_dialog.current_audio_language
                    self.data[row_index].audio_track_name = audio_info_dialog.current_audio_track_name
                    self.data[row_index].audio_set_default = audio_info_dialog.current_audio_set_default
                    self.data[row_index].audio_set_forced = audio_info_dialog.current_audio_set_forced
                    current_cell_widget = self.cellWidget(row_index, self.column_ids["Audio"])
                    if len(audio_info_dialog.current_audio_delay) == 1:
                        current_cell_widget.update_tool_tip(tool_tip=generate_tool_tip_for_audio_file(
                            audio_full_path=GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[0][row_index],
                            audio_name=GlobalSetting.AUDIO_FILES_LIST[0][row_index],
                            audio_delay=self.data[row_index].audio_delay[0],
                            audio_language=self.data[row_index].audio_language[0],
                            audio_track_name=self.data[row_index].audio_track_name[0],
                            audio_set_default=self.data[row_index].audio_set_default[0],
                            audio_set_forced=self.data[row_index].audio_set_forced[0],
                            show_full_path=False))

            else:
                warning_dialog = WarningDialog(window_title="Audio Info", info_message="No audio found!")
                warning_dialog.execute()
        elif column_index == self.column_ids["Chapter"]:
            if self.data[row_index].chapter_found:
                chapter_info_dialog = ChapterInfoDialog(chapter_name=self.data[row_index].chapter_name)
                chapter_info_dialog.execute()
            else:
                warning_dialog = WarningDialog(window_title="Chapter Info", info_message="No chapter found!")
                warning_dialog.execute()
        elif column_index == self.column_ids["Status"]:
            if self.data[row_index].error_occurred:
                message = self.data[row_index].muxing_message
                message += "you can review log file for more details"
                error_muxing_dialog = ErrorMuxingDialog(window_title="Muxing Error", info_message=message)
                error_muxing_dialog.execute()
            elif self.data[row_index].done:
                Ok_dialog = OkDialog(window_title="Muxing Done")
                Ok_dialog.execute()

    def show_necessary_columns(self):
        if not GlobalSetting.AUDIO_ENABLED:
            self.hideColumn(self.column_ids["Audio"])
        else:
            self.showColumn(self.column_ids["Audio"])
        if not GlobalSetting.SUBTITLE_ENABLED:
            self.hideColumn(self.column_ids["Subtitle"])
        else:
            self.showColumn(self.column_ids["Subtitle"])
        if len(GlobalSetting.CHAPTER_FILES_LIST) == 0:
            self.hideColumn(self.column_ids["Chapter"])
        else:
            self.showColumn(self.column_ids["Chapter"])

    def update_widget(self):
        if self.need_column_width_set:
            header_width = self.horizontal_header.width()
            self.horizontal_header.setMinimumSectionSize(header_width * 4 // 25)
            self.setColumnWidth(0, int(header_width * 8) // 10)
            self.need_column_width_set = False

        if self.columnWidth(0) > screen_size.width() // 7:
            self.setColumnWidth(1, screen_size.width() // 14)
        else:
            self.setColumnWidth(
                1, self.columnWidth(0) // 2
            )

    def setup_queue(self):
        self.clear_queue()
        self.hide()
        self.setRowCount(len(GlobalSetting.VIDEO_FILES_LIST))
        for i in range(len(GlobalSetting.VIDEO_FILES_LIST)):
            new_row_id = i
            new_job = SingleJobData()
            self.set_row_value_id(new_row_id)
            self.set_row_value_name(new_job, new_row_id)
            self.set_row_value_audio(new_job, new_row_id)
            self.set_row_value_subtitle(new_job, new_row_id)
            self.set_row_value_chapter(new_job, new_row_id)
            self.set_row_value_size_before_muxing(new_job, new_row_id)
            self.set_row_value_progressBar(new_job, new_row_id)
            set_is_job_crc_required(new_job)
            set_attachments_setting_for_job(new_job, new_row_id)
            self.data.append(new_job)
        self.show()
        self.check_if_name_need_resize_column_to_fit_content()
        # self.resize_name_column_to_fit_content()
        self.update_widget()
        self.total_progress = 0
        self.update_total_progress_signal.emit(0)
        self.number_of_jobs = len(self.data)
        self.number_of_done_jobs = 0
        self.set_number_of_jobs_signal.emit(self.number_of_jobs)
        if len(self.data) > 0:
            GlobalSetting.JOB_QUEUE_EMPTY = False
        else:
            GlobalSetting.JOB_QUEUE_EMPTY = True

    # noinspection PyAttributeOutsideInit
    def start_muxing(self):
        self.start_muxing_thread = QThread()
        self.start_muxing_worker = StartMuxingWorker(self.data)
        self.start_muxing_worker.moveToThread(self.start_muxing_thread)
        self.start_muxing_thread.started.connect(self.start_muxing_worker.run)
        self.start_muxing_worker.finished_paused_signal.connect(self.start_muxing_thread.quit)
        self.start_muxing_worker.finished_all_jobs_signal.connect(self.start_muxing_thread.quit)
        self.start_muxing_worker.finished_all_jobs_signal.connect(self.start_muxing_worker.deleteLater)
        self.start_muxing_worker.finished_all_jobs_signal.connect(self.finished_all_jobs)
        self.start_muxing_worker.finished_paused_signal.connect(self.start_muxing_worker.deleteLater)
        self.start_muxing_worker.finished_paused_signal.connect(self.paused_done)
        self.start_muxing_worker.cancel_signal.connect(self.start_muxing_thread.quit)
        self.start_muxing_worker.cancel_signal.connect(self.start_muxing_worker.deleteLater)
        self.start_muxing_thread.finished.connect(self.start_muxing_thread.deleteLater)
        self.start_muxing_worker.mkvpropedit_good_signal.connect(self.show_confirm_using_mkvpropedit)
        self.start_muxing_worker.progress_signal.connect(self.update_progress)
        self.start_muxing_worker.job_started_signal.connect(self.new_job_started)
        self.start_muxing_worker.job_succeeded_signal.connect(self.job_done_successfully)
        self.start_muxing_worker.job_failed_signal.connect(self.job_error_occurred)
        self.start_muxing_worker.pause_from_error_occurred_signal.connect(self.pause_from_error_occurred)
        self.start_muxing_worker.crc_progress_signal.connect(self.update_crc_progress)
        self.start_muxing_thread.start()

    def clear_queue(self):
        self.data = []  # type: list[SingleJobData]
        self.setRowCount(0)
        self.total_progress = 0
        self.number_of_jobs = 0
        self.number_of_done_jobs = 0
        GlobalSetting.JOB_QUEUE_EMPTY = True

    def show_confirm_using_mkvpropedit(self):
        confirm_dialog = ConfirmUsingMkvpropedit()
        confirm_dialog.execute()
        if confirm_dialog.result == "mkvpropedit":
            self.start_muxing_worker.use_mkvpropedit = True
            self.start_muxing_worker.waiting_for_mkvpropedit_confirm = False
        elif confirm_dialog.result == "mkvmerge":
            self.start_muxing_worker.use_mkvpropedit = False
            self.start_muxing_worker.use_mkvmerge = True
            self.start_muxing_worker.waiting_for_mkvpropedit_confirm = False
        else:
            self.start_muxing_worker.cancel = True
            self.start_muxing_worker.use_mkvpropedit = False
            self.start_muxing_worker.use_mkvmerge = False
            self.start_muxing_worker.waiting_for_mkvpropedit_confirm = False
            if self.start_muxing_worker.current_job == 0:
                self.cancel_done_signal.emit()
            else:
                self.paused_done_signal.emit()

    def update_progress(self, params: MuxingParams):
        job_index = params.index
        new_progress = params.progress
        if params.error:
            self.data[job_index].done = True
            self.data[job_index].error_occurred = True
            self.data[job_index].muxing_message = params.message
            if GlobalSetting.MUX_SETTING_ABORT_ON_ERRORS:
                self.start_muxing_worker.pause = True
            self.set_job_status_bad(row_index=job_index)
            self.update_muxing_progress(job_index, 0, params)
        else:
            self.update_muxing_progress(job_index, new_progress, params)

    def update_crc_progress(self, progress):
        self.update_status_job_widget("CRC: " + str(progress))

    def get_output_file_name_absolute(self, job_index):
        if self.data[job_index].used_mkvpropedit:
            return Path(self.data[job_index].video_name_absolute)
        else:
            folder_path = Path(GlobalSetting.DESTINATION_FOLDER_PATH)
            output_video_name = Path(get_file_name_with_mkv_extension(self.data[job_index].video_name))
            return os.path.join(folder_path, output_video_name)

    def get_output_file_name_folder_path_absolute(self, job_index):
        if self.data[job_index].used_mkvpropedit or GlobalSetting.OVERWRITE_SOURCE_FILES:
            return os.path.dirname(self.data[job_index].video_name_absolute)

        else:
            return Path(GlobalSetting.DESTINATION_FOLDER_PATH)

    def update_muxing_progress(self, job_index, new_progress, params):
        self.total_progress -= self.data[job_index].progress
        self.data[job_index].progress = new_progress
        self.update_status_job_widget(new_progress)
        self.total_progress += self.data[job_index].progress
        self.cellWidget(params.index, self.column_ids["Progress"]).setValue(new_progress)
        self.update_total_progress_signal.emit(self.total_progress // self.number_of_jobs)

    def update_status_job_widget(self, new_progress):
        try:
            self.job_status_widget.update_progress(new_progress=new_progress)
        except:
            pass

    def delete_source_file_if_overwritten_enabled(self, job_index):
        if GlobalSetting.OVERWRITE_SOURCE_FILES and not self.data[job_index].used_mkvpropedit:
            os.remove(self.data[job_index].video_name_absolute)
            folder_path = os.path.dirname(self.data[job_index].video_name_absolute)
            output_video_name = Path(change_file_extension_to_mkv_with_random_suffix(self.data[job_index].video_name))
            output_video_name_absolute = os.path.join(folder_path, output_video_name)
            original_output_video_name = Path(get_file_name_with_mkv_extension(self.data[job_index].video_name))
            output_file_name_folder_path_absolute = self.get_output_file_name_folder_path_absolute(job_index)
            original_file_name_absolute_path = os.path.join(output_file_name_folder_path_absolute,
                                                            original_output_video_name)
            rename_file(output_video_name_absolute, original_file_name_absolute_path)

    def rename_output_file_if_needed(self, job_index):
        if self.data[job_index].is_crc_calculating_required:
            crc_string = self.data[job_index].new_crc
            output_video_name = Path(get_file_name_with_mkv_extension(self.data[job_index].video_name))
            file_name_with_crc = Path(get_file_name_with_crc(output_video_name, crc_string))
            output_file_name_folder_path_absolute = self.get_output_file_name_folder_path_absolute(job_index)
            file_name_with_crc_absolute_path = os.path.join(output_file_name_folder_path_absolute, file_name_with_crc)
            file_name_old_crc_absolute_path = os.path.join(output_file_name_folder_path_absolute, output_video_name)
            rename_file(file_name_old_crc_absolute_path, file_name_with_crc_absolute_path)
            self.data[job_index].output_video_name = file_name_with_crc
            self.data[job_index].output_video_absolute_path = file_name_with_crc_absolute_path
        elif self.data[job_index].is_crc_removing_required:
            output_video_name = Path(get_file_name_with_mkv_extension(self.data[job_index].video_name))
            output_file_name_folder_path_absolute = self.get_output_file_name_folder_path_absolute(job_index)
            file_name_old_absolute_path = os.path.join(output_file_name_folder_path_absolute, output_video_name)
            file_name_without_crc = Path(get_file_name_without_crc(output_video_name))
            file_name_without_crc_absolute_path = os.path.join(output_file_name_folder_path_absolute,
                                                               file_name_without_crc)
            rename_file(file_name_old_absolute_path, file_name_without_crc_absolute_path)
            self.data[job_index].output_video_name = file_name_without_crc
            self.data[job_index].output_video_absolute_path = file_name_without_crc_absolute_path
        else:
            output_video_name = Path(get_file_name_with_mkv_extension(self.data[job_index].video_name))
            output_file_name_folder_path_absolute = self.get_output_file_name_folder_path_absolute(job_index)
            file_name_absolute_path = os.path.join(output_file_name_folder_path_absolute, output_video_name)
            self.data[job_index].output_video_name = output_video_name
            self.data[job_index].output_video_absolute_path = file_name_absolute_path

    def job_done_successfully(self, job_index):
        self.data[job_index].done = True
        self.number_of_done_jobs += 1
        self.increase_number_of_done_jobs_signal.emit()
        self.set_job_status_ok(row_index=job_index)
        self.delete_source_file_if_overwritten_enabled(job_index=job_index)
        self.rename_output_file_if_needed(job_index=job_index)
        self.set_row_value_size_after_muxing(self.data[job_index], job_index)

    def job_error_occurred(self, job_index):
        self.data[job_index].done = True
        self.data[job_index].error_occurred = True
        if GlobalSetting.MUX_SETTING_ABORT_ON_ERRORS:
            self.start_muxing_worker.pause = True
        self.set_job_status_bad(row_index=job_index)
        self.rename_output_file_if_needed(job_index=job_index)
        self.set_row_value_size_after_muxing(self.data[job_index], job_index)

    def set_job_status_ok(self, row_index):
        self.job_status_widget.stop_loading()
        self.cellWidget(row_index, self.column_ids["Status"]).deleteLater()
        self.setCellWidget(row_index, self.column_ids["Status"], OkCell(tool_tip="Done"))

    def set_job_status_bad(self, row_index):
        self.job_status_widget.stop_loading()
        self.cellWidget(row_index, self.column_ids["Status"]).deleteLater()
        self.setCellWidget(row_index, self.column_ids["Status"], ErrorCell(tool_tip="Error Happened\nDouble click for "
                                                                                    "more details"))

    # noinspection PyAttributeOutsideInit
    def new_job_started(self, row_index):
        self.job_status_widget = StatusWidget()
        self.setCellWidget(row_index, self.column_ids["Status"], self.job_status_widget)
        self.job_status_widget.start_loading()

    def pause_muxing(self):
        self.start_muxing_worker.pause = True

    def paused_done(self):
        self.paused_done_signal.emit()

    def finished_all_jobs(self):
        self.finished_all_jobs_signal.emit()

    def pause_from_error_occurred(self):
        self.pause_from_error_occurred_signal.emit()

    def delete_video_output_with_zero_size(self, file_path):
        try:
            os.remove(file_path)
        except:
            pass
