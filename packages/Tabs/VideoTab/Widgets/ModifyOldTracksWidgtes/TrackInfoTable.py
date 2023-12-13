from typing import List

import PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QLabel

from packages.Tabs.VideoTab.Widgets.ModifyOldTracksWidgtes.TrackInfoTableColumnsID import TrackInfoTableColumnsID
from packages.Widgets.GreenTikCell import GreenTikCell
from packages.Widgets.RedCrossCell import RedCrossCell
from packages.Widgets.SingleOldTrackData import SingleOldTrackData
from packages.Widgets.TableWidget import TableWidget


class TrackInfoTable(TableWidget):
    def __init__(self):
        super().__init__()
        self.column_ids = TrackInfoTableColumnsID()
        self.setColumnCount(len(self.column_ids.columns_name))
        self.horizontal_header = None
        self.tracks_info: List[List[SingleOldTrackData]] = [[]]
        self.video_names = []
        self.setRowCount(0)
        self.force_no_selection()
        self.create_horizontal_header()
        self.setup_horizontal_header()
        self.setup_columns()
        self.connect_signals()

    def connect_signals(self):
        self.horizontalHeader().sectionResized.connect(self.check_if_video_name_need_resize_column_to_fit_content)
        self.horizontalHeader().sectionResized.connect(self.check_if_track_name_need_resize_column_to_fit_content)

    def setup_columns(self):
        for column_id in range(len(self.column_ids.columns_name)):
            self.set_column_name(column_index=column_id, name=self.column_ids.columns_name[column_id])

    def set_column_name(self, column_index, name):
        column = QTableWidgetItem(name)
        column.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setHorizontalHeaderItem(column_index, column)

    def force_no_selection(self):
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    def create_horizontal_header(self):
        self.horizontal_header = self.horizontalHeader()

    def setup_horizontal_header(self):
        self.horizontal_header.setSectionResizeMode(self.column_ids.Video_Name, QHeaderView.ResizeMode.Interactive)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Found, QHeaderView.ResizeMode.Fixed)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Is_Default, QHeaderView.ResizeMode.Fixed)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Is_Forced, QHeaderView.ResizeMode.Fixed)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Track_Name, QHeaderView.ResizeMode.Interactive)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Track_Language, QHeaderView.ResizeMode.Stretch)

    def set_row_value_video_name(self, row_id, video_name):
        item = QTableWidgetItem(video_name)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(row_id, self.column_ids.Video_Name, item)

    def set_row_value_empty_cell(self, row_id, column_id):
        self.setCellWidget(row_id, column_id, QLabel())

    def set_row_value_empty_item(self, row_id, column_id):
        item = QTableWidgetItem(" ")
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(row_id, column_id, item)

    def set_row_value_found_track(self, row_id, found):
        if found:
            self.setCellWidget(row_id, self.column_ids.Found, GreenTikCell(tool_tip="Track Found"))
        else:
            self.setCellWidget(row_id, self.column_ids.Found, RedCrossCell(tool_tip="Track Not Found"))

    def set_row_value_is_default_track(self, row_id, is_default):
        if is_default:
            self.setCellWidget(row_id, self.column_ids.Is_Default, GreenTikCell(tool_tip="The track is default"))
        else:
            self.setCellWidget(row_id, self.column_ids.Is_Default, RedCrossCell(tool_tip="The track is not default"))

    def set_row_value_is_forced_track(self, row_id, is_forced):
        if is_forced:
            self.setCellWidget(row_id, self.column_ids.Is_Forced, GreenTikCell(tool_tip="The track is forced"))
        else:
            self.setCellWidget(row_id, self.column_ids.Is_Forced, RedCrossCell(tool_tip="The track is not default"))

    def set_row_value_track_name(self, new_row_id, track_name):
        item = QTableWidgetItem(track_name)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(new_row_id, self.column_ids.Track_Name, item)

    def set_row_value_track_language(self, new_row_id, track_language):
        item = QTableWidgetItem(track_language)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(new_row_id, self.column_ids.Track_Language, item)

    def setup_video_names(self):
        self.setRowCount(len(self.video_names))
        for new_row_id in range(len(self.video_names)):
            self.set_row_value_video_name(new_row_id, self.video_names[new_row_id])

    def setup_info(self, track_id):
        for new_row_id in range(len(self.video_names)):
            found_track = False
            for track in self.tracks_info[new_row_id]:
                if int(track.id) == int(track_id):
                    self.set_row_value_found_track(new_row_id, True)
                    self.set_row_value_is_default_track(new_row_id, track.is_default)
                    self.set_row_value_is_forced_track(new_row_id, track.is_forced)
                    self.set_row_value_track_name(new_row_id, track.track_name)
                    self.set_row_value_track_language(new_row_id, track.language)
                    found_track = True
                    break
            if not found_track:
                self.set_row_value_found_track(new_row_id, False)
                self.set_row_value_empty_cell(new_row_id, self.column_ids.Is_Default)
                self.set_row_value_empty_cell(new_row_id, self.column_ids.Is_Forced)
                self.set_row_value_empty_item(new_row_id, self.column_ids.Track_Name)
                self.set_row_value_empty_item(new_row_id, self.column_ids.Track_Language)

        self.check_if_video_name_need_resize_column_to_fit_content()
        self.check_if_track_name_need_resize_column_to_fit_content()
        self.resizeColumnToContents(self.column_ids.Track_Language)

    def check_if_video_name_need_resize_column_to_fit_content(self):
        new_column_width = 0
        for i in range(self.rowCount()):
            column_font = self.item(i, self.column_ids.Video_Name).font()
            column_font_metrics = QFontMetrics(column_font)
            new_column_width = max(new_column_width,
                                   column_font_metrics.horizontalAdvance(self.video_names[i]))
        new_column_width += 10
        if new_column_width >= self.columnWidth(self.column_ids.Video_Name):
            self.setColumnWidth(self.column_ids.Video_Name, new_column_width)

    def check_if_track_name_need_resize_column_to_fit_content(self):

        new_column_width = 0
        for i in range(self.rowCount()):
            item = self.item(i, self.column_ids.Track_Name)
            if item is None:
                continue
            column_font = item.font()
            column_font_metrics = QFontMetrics(column_font)
            new_column_width = max(new_column_width,
                                   column_font_metrics.horizontalAdvance(
                                       self.item(i, self.column_ids.Track_Name).text()))
        new_column_width += 10
        if self.columnWidth(self.column_ids.Track_Name) < 100 or new_column_width < 100:
            new_column_width = 100
        if new_column_width >= self.columnWidth(self.column_ids.Track_Name):
            self.setColumnWidth(self.column_ids.Track_Name, new_column_width)

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent):
        super().resizeEvent(event)
        self.check_if_video_name_need_resize_column_to_fit_content()
        self.check_if_track_name_need_resize_column_to_fit_content()

    def update_video_name(self, new_video_names_list):
        self.video_names = new_video_names_list.copy()
        self.setup_video_names()

    def update_tracks_info(self, new_tracks_info_list):
        self.tracks_info = new_tracks_info_list.copy()
