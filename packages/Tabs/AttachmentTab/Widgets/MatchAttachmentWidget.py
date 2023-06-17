import logging
import os
from typing import List

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QHBoxLayout, QWidget

from packages.Tabs.AttachmentTab.Widgets.AttachmentMatchingTable import AttachmentMatchingTable
from packages.Tabs.AttachmentTab.Widgets.MatchAttachmentToolsLayout import MatchAttachmentToolsLayout
from packages.Widgets.PathData import PathData
from packages.Tabs.AttachmentTab.Widgets.VideoMatchingTable import VideoMatchingTable
from packages.Tabs.GlobalSetting import GlobalSetting, get_readable_filesize, sort_names_like_windows


class MatchAttachmentWidget(QWidget):
    drag_and_dropped_signal = Signal()
    update_total_size_readable_signal = Signal(str)
    is_there_old_paths_signal = Signal(bool)

    def __init__(self, parent=None):
        super().__init__()
        self.video_table = VideoMatchingTable()
        self.attachment_table = AttachmentMatchingTable()
        self.paths_list: List[PathData] = []
        self.total_size_bytes = 0
        self.match_tools_layout = MatchAttachmentToolsLayout(parent=parent)
        self.sync_slideBar_check = False
        self.attachment_table.setAcceptDrops(True)
        self.connect_signals()
        self.main_layout = QHBoxLayout()
        self.setup_layout()
        self.hide()

    def connect_signals(self):
        self.attachment_table.selectionModel().selectionChanged.connect(
            self.sync_selection_between_attachments_and_videos
        )
        self.attachment_table.selectionModel().selectionChanged.connect(
            self.send_selection_to_tools_layout
        )
        self.match_tools_layout.refresh_attachment_table_signal.connect(
            self.show_attachment_files_after_swapping_deleting)
        self.match_tools_layout.selected_attachment_row_signal.connect(self.change_selected_attachment_row)
        self.attachment_table.drop_folder_and_files_signal.connect(self.update_paths_with_drag_and_drop)

    def setup_layout(self):
        self.main_layout.addWidget(self.video_table, 50)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.match_tools_layout, 4)
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(self.attachment_table, 50)
        self.setLayout(self.main_layout)

    def sync_slideBar(self):
        if self.sync_slideBar_check or self.attachment_table.verticalScrollBar().isSliderDown():
            self.video_table.table.verticalScrollBar().setValue(
                self.attachment_table.verticalScrollBar().value()
            )
            self.sync_slideBar_check = False

    def sync_selection_between_attachments_and_videos(self):
        list_of_selected_rows = self.attachment_table.selectionModel().selectedRows()
        video_file_list = GlobalSetting.VIDEO_FILES_LIST
        if len(list_of_selected_rows):
            selected_row = list_of_selected_rows[0].row()
            if len(video_file_list) - 1 >= selected_row:
                self.video_table.table.preventSelect = False
                oldHorizontalScrollBarValue = (
                    self.video_table.table.horizontalScrollBar().value()
                )
                self.video_table.table.selectRow(selected_row)
                self.video_table.table.horizontalScrollBar().setValue(
                    oldHorizontalScrollBarValue
                )
                self.video_table.table.preventSelect = True
                self.sync_slideBar_check = True
            else:
                self.video_table.table.clearSelection()
                return
        else:
            self.video_table.table.clearSelection()
            return

    def send_selection_to_tools_layout(self):
        selected_row = -1
        max_index = len(GlobalSetting.ATTACHMENT_PATH_DATA_LIST) - 1
        list_of_selected_rows = self.attachment_table.selectionModel().selectedRows()
        if len(list_of_selected_rows) > 0:
            selected_row = list_of_selected_rows[0].row()
        self.match_tools_layout.set_selected_row(selected_row=selected_row, max_index=max_index)

    def show_video_files(self):
        self.video_table.show_files()

    def show_attachment_files_after_swapping_deleting(self):
        self.sync_attachment_files_with_global_files_after_swap_delete()
        self.attachment_table.show_paths_list(path_list=self.paths_list)

    def sync_attachment_files_with_global_files_after_swap_delete(self):
        self.paths_list = GlobalSetting.ATTACHMENT_PATH_DATA_LIST
        self.update_total_size()
        self.update_is_there_old_paths()

    def change_selected_attachment_row(self, new_selected_row):
        self.attachment_table.select_row(new_selected_row)

    def clear_attachment_table(self):
        self.paths_list.clear()
        self.attachment_table.clear_table()

    def clear_attachment_selection(self):
        self.attachment_table.clear_selection()

    def disable_editable_widgets(self):
        self.attachment_table.setAcceptDrops(False)
        self.match_tools_layout.disable_editable_widgets()

    def enable_editable_widgets(self):
        self.attachment_table.setAcceptDrops(True)
        self.match_tools_layout.enable_editable_widgets()

    def update_paths(self, path):
        self.clear_paths()
        paths_list = sort_names_like_windows(os.listdir(path))
        paths_list = [os.path.join(path, file) for file in paths_list]
        for path in paths_list:
            if os.path.isdir(path):
                try:
                    temp_path = PathData()
                    temp_path.name = os.path.basename(path)
                    temp_path.absolute_name = path
                    temp_path.files_list = [os.path.join(path, file) for file in os.listdir(path)]
                    temp_path.files_list = [file for file in temp_path.files_list if
                                            os.path.isfile(file) and os.path.getsize(file) != 0]
                    total_size = 0
                    for file in temp_path.files_list:
                        file_name_absolute = file
                        file_size_bytes = os.path.getsize(file_name_absolute)
                        total_size += file_size_bytes
                    temp_path.total_size = total_size
                    self.paths_list.append(temp_path)
                except Exception as e:
                    logging.error(e)
                    continue
            else:
                try:
                    if os.path.getsize(path) == 0:
                        continue
                    temp_path = PathData()
                    temp_path.name = os.path.basename(path)
                    temp_path.absolute_name = path
                    temp_path.files_list = [path]
                    temp_path.total_size = os.path.getsize(path)
                    self.paths_list.append(temp_path)
                except Exception as e:
                    logging.error(e)
                    continue
        self.attachment_table.show_paths_list(path_list=self.paths_list.copy())
        GlobalSetting.ATTACHMENT_PATH_DATA_LIST = self.paths_list.copy()
        self.update_total_size()
        self.update_is_there_old_paths()

    def update_paths_with_drag_and_drop(self, paths_list):
        for path in paths_list:
            if os.path.isdir(path):
                try:
                    temp_path = PathData()
                    temp_path.name = os.path.basename(path)
                    temp_path.absolute_name = path
                    temp_path.files_list = [os.path.join(path, file) for file in os.listdir(path)]
                    temp_path.files_list = [file for file in temp_path.files_list if
                                            os.path.isfile(file) and os.path.getsize(file) != 0]
                    total_size = 0
                    for file in temp_path.files_list:
                        file_name_absolute = file
                        file_size_bytes = os.path.getsize(file_name_absolute)
                        total_size += file_size_bytes
                    temp_path.total_size = total_size
                    self.paths_list.append(temp_path)
                except Exception as e:
                    logging.error(e)
                    continue
            else:
                try:
                    if os.path.getsize(path) == 0:
                        continue
                    temp_path = PathData()
                    temp_path.name = os.path.basename(path)
                    temp_path.absolute_name = path
                    temp_path.files_list = [path]
                    temp_path.total_size = os.path.getsize(path)
                    self.paths_list.append(temp_path)
                except Exception as e:
                    logging.error(e)
                    continue
        self.attachment_table.show_paths_list(path_list=self.paths_list.copy())
        GlobalSetting.ATTACHMENT_PATH_DATA_LIST = self.paths_list.copy()
        self.drag_and_dropped_signal.emit()
        self.update_total_size()
        self.update_is_there_old_paths()
        # self.is_drag_and_drop = True
        # self.folder_path = ""
        # self.chapter_source_lineEdit.stop_check_path = True
        # self.chapter_source_lineEdit.setText(self.drag_and_dropped_text)

    def update_total_size(self):
        self.total_size_bytes = 0
        for path in self.paths_list:
            self.total_size_bytes += path.total_size
        self.update_total_size_readable_signal.emit(get_readable_filesize(self.total_size_bytes))

    def clear_paths(self):
        self.paths_list.clear()
        GlobalSetting.ATTACHMENT_PATH_DATA_LIST.clear()
        self.attachment_table.show_paths_list(path_list=self.paths_list)
        self.total_size_bytes = 0
        self.update_is_there_old_paths()

    def update_is_there_old_paths(self):
        self.is_there_old_paths_signal.emit(len(self.paths_list) > 0)
