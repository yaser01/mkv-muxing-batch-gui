import typing
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFontMetrics, QColor, QKeySequence, QShortcut
from PySide6.QtWidgets import QAbstractItemView, QTableWidgetItem, QHeaderView, QComboBox

from packages.Startup.Options import Options
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Tabs.GlobalSetting import convert_string_integer_to_two_digit_string, GlobalSetting
from packages.Tabs.VideoTab.Widgets.ModifyOldTracksWidgtes.CenteredCheckBoxCell import CenteredCheckBoxCell
from packages.Tabs.VideoTab.Widgets.ModifyOldTracksWidgtes.ModifyOldTracksTableColumnsID import \
    ModifyOldTracksTableColumnsID
from packages.Widgets.SingleOldTrackData import SingleOldTrackData
from packages.Widgets.TableWidget import TableWidget


class OldTracksTable(TableWidget):
    selected_track_changed = Signal(int)

    def __init__(self, original_setting, current_setting, tracks_info, all_languages):
        super().__init__()
        self.text_color = {"light": {"activate": "#000000", "disable": "#787878"},
                           "dark": {"activate": "#FFFFFF", "disable": "#878787"}}
        self.column_ids = ModifyOldTracksTableColumnsID()
        self.original_setting: typing.Dict[str, SingleOldTrackData] = original_setting
        self.current_setting: typing.Dict[str, SingleOldTrackData] = current_setting
        self.all_languages = all_languages
        self.tracks_info = tracks_info
        self.horizontal_header = None
        self.move_row_up_shortcut = None
        self.move_row_down_shortcut = None
        self.need_column_width_set = True
        self.is_there_different_track_setting = False
        self.is_there_deleted_tracks = False
        self.is_there_reorder_tracks = False
        self.setColumnCount(len(self.column_ids.columns_name))
        self.setRowCount(0)
        self.force_select_whole_row()
        self.force_single_row_selection()
        self.disable_table_bold_column()
        self.create_horizontal_header()
        self.setup_horizontal_header()
        self.setup_shortcuts()
        self.setup_columns()
        self.setup_tracks()
        self.check_if_job_queue_not_empty()
        self.connect_signals()

    def create_horizontal_header(self):
        self.horizontal_header = self.horizontalHeader()

    def setup_shortcuts(self):
        self.move_row_up_shortcut = QShortcut(QKeySequence("Ctrl+Up"), self)
        self.move_row_down_shortcut = QShortcut(QKeySequence("Ctrl+Down"), self)

    def connect_signals(self):
        self.itemChanged.connect(self.item_changed)
        self.currentCellChanged.connect(self.update_selected_track)
        if GlobalSetting.JOB_QUEUE_EMPTY:
            self.move_row_up_shortcut.activated.connect(self.move_row_up)
            self.move_row_down_shortcut.activated.connect(self.move_row_down)

    def setup_columns(self):
        for column_id in range(len(self.column_ids.columns_name)):
            self.set_column_name(column_index=column_id, name=self.column_ids.columns_name[column_id])

    def set_column_name(self, column_index, name):
        column = QTableWidgetItem(name)
        column.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setHorizontalHeaderItem(column_index, column)

    def disable_table_bold_column(self):
        self.horizontalHeader().setHighlightSections(False)

    def force_select_whole_row(self):
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    def force_single_row_selection(self):
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def setup_horizontal_header(self):
        self.horizontal_header.setSectionResizeMode(self.column_ids.ID, QHeaderView.ResizeMode.Fixed)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Enable, QHeaderView.ResizeMode.Fixed)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Set_Default, QHeaderView.ResizeMode.Fixed)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Set_Forced, QHeaderView.ResizeMode.Fixed)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Track_Name, QHeaderView.ResizeMode.Interactive)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Track_Language, QHeaderView.ResizeMode.Stretch)

    def setup_tracks(self):
        is_there_different_track_setting = False
        is_there_deleted_tracks = False
        is_there_reorder_tracks = False
        self.setRowCount(len(self.current_setting.keys()))
        for new_row_id, track_id in enumerate(self.current_setting.keys(), start=0):
            new_row_id = self.current_setting[track_id].order
            is_enabled_state = self.current_setting[track_id].is_enabled
            is_default_state = self.current_setting[track_id].is_default
            is_forced_state = self.current_setting[track_id].is_forced
            track_name = self.current_setting[track_id].track_name
            language = self.current_setting[track_id].language
            self.set_row_value_id(track_id, new_row_id)
            self.set_row_value_is_enabled(is_enabled_state, new_row_id)
            self.set_row_value_is_default(is_default_state, new_row_id)
            self.set_row_value_is_forced(is_forced_state, new_row_id)
            self.set_row_value_track_name(track_name, new_row_id)
            self.set_row_value_language(language, new_row_id)
            self.update_state_of_row(new_row_id, is_enabled_state)
            if not is_there_different_track_setting and self.current_setting[track_id] != self.original_setting[
                track_id]:
                is_there_different_track_setting = True
            if not self.current_setting[track_id].is_enabled:
                is_there_deleted_tracks = True
            if self.current_setting[track_id].order != self.original_setting[track_id].order:
                is_there_reorder_tracks = True
        self.update_widget()
        self.resize_track_name_column_to_fit_content()
        self.is_there_different_track_setting = is_there_different_track_setting
        self.is_there_deleted_tracks = is_there_deleted_tracks
        self.is_there_reorder_tracks = is_there_reorder_tracks

    def check_if_job_queue_not_empty(self):
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            for row_id in range(self.rowCount()):
                self.cellWidget(row_id, self.column_ids.Enable).check_box.setEnabled(False)
                self.cellWidget(row_id, self.column_ids.Set_Default).check_box.setEnabled(False)
                self.cellWidget(row_id, self.column_ids.Set_Forced).check_box.setEnabled(False)
                self.item(row_id, self.column_ids.Track_Name).setFlags(
                    self.item(row_id, self.column_ids.Track_Name).flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.cellWidget(row_id, self.column_ids.Track_Language).setEnabled(False)

    def set_row_value_id(self, track_id, new_row_id):
        item = QTableWidgetItem("Track " + convert_string_integer_to_two_digit_string(track_id))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(new_row_id, self.column_ids.ID, item)

    def set_row_value_is_enabled(self, is_enabled_state, new_row_id):
        check_box = CenteredCheckBoxCell(row_id=new_row_id, column_id=self.column_ids.Enable,
                                         check_state=is_enabled_state, parent=self)
        self.setCellWidget(new_row_id, self.column_ids.Enable, check_box)
        check_box.signal_state_changed.connect(self.check_box_state_changed)

    def set_row_value_is_default(self, is_default_state, new_row_id):
        check_box = CenteredCheckBoxCell(row_id=new_row_id, column_id=self.column_ids.Set_Default,
                                         check_state=is_default_state, parent=self)
        check_box.signal_state_changed.connect(self.check_box_state_changed)
        self.setCellWidget(new_row_id, self.column_ids.Set_Default, check_box)

    def set_row_value_is_forced(self, is_forced_state, new_row_id):
        check_box = CenteredCheckBoxCell(row_id=new_row_id, column_id=self.column_ids.Set_Forced,
                                         check_state=is_forced_state, parent=self)
        self.setCellWidget(new_row_id, self.column_ids.Set_Forced, check_box)
        check_box.signal_state_changed.connect(self.check_box_state_changed)

    def set_row_value_track_name(self, track_name, new_row_id):
        item = QTableWidgetItem(track_name)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setItem(new_row_id, self.column_ids.Track_Name, item)

    def set_row_value_language(self, language, new_row_id):
        combo_box = QComboBox(parent=self)
        combo_box.addItems(self.all_languages)
        if language in self.all_languages:
            combo_box.setCurrentIndex(self.all_languages.index(language))
        else:
            combo_box.setCurrentIndex(-1)
        combo_box.setMaxVisibleItems(8)
        combo_box.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.setCellWidget(new_row_id, self.column_ids.Track_Language, combo_box)

    def update_widget(self):
        if self.need_column_width_set:
            header_width = self.horizontal_header.width()
            self.horizontal_header.setMinimumSectionSize(header_width * 5 // 25)
            self.need_column_width_set = False

        if self.columnWidth(0) > screen_size.width() // 7:
            self.setColumnWidth(1, screen_size.width() // 14)
        else:
            self.setColumnWidth(
                1, self.columnWidth(0) // 2
            )

    def resize_track_name_column_to_fit_content(self):
        # Resize track_name Column Only
        new_column_width = 0
        for i in range(self.rowCount()):
            column_font = self.item(i, self.column_ids.Track_Name).font()
            column_font_metrics = QFontMetrics(column_font)
            new_column_width = max(new_column_width,
                                   column_font_metrics.horizontalAdvance(
                                       self.item(i, self.column_ids.Track_Name).text()))
        new_column_width += 10
        if new_column_width != 0:
            self.setColumnWidth(self.column_ids.Track_Name, new_column_width)

    def item_changed(self, item: QTableWidgetItem):
        if item.column() == self.column_ids.Track_Name:
            pass

    def get_track_id_of_row(self, row_id):
        for new_row_id, track_id in enumerate(self.current_setting.keys(), start=0):
            if new_row_id == row_id:
                return track_id
        return -1

    def get_text_color(self, status):
        if status:
            status = "activate"
        else:
            status = "disable"
        if Options.Dark_Mode:
            new_color = QColor(self.text_color["dark"][status])
        else:
            new_color = QColor(self.text_color["light"][status])
        return new_color

    def check_box_state_changed(self, new_change_list: list):
        row_id, column_id, new_state = new_change_list
        if column_id == self.column_ids.Enable:
            if new_state == Qt.CheckState.Checked.value:
                new_state = True
            else:
                new_state = False
            self.update_state_of_row(row_id, new_state)
        elif column_id == self.column_ids.Set_Default:
            if new_state == Qt.CheckState.Checked.value:
                for i in range(self.rowCount()):
                    if i == row_id:
                        continue
                    self.cellWidget(i, column_id).check_box.setCheckState(Qt.CheckState.Unchecked)
        elif column_id == self.column_ids.Set_Forced:
            if new_state == Qt.CheckState.Checked.value:
                for i in range(self.rowCount()):
                    if i == row_id:
                        continue
                    self.cellWidget(i, column_id).check_box.setCheckState(Qt.CheckState.Unchecked)

    def update_state_of_row(self, row_id, new_state):
        self.cellWidget(row_id, self.column_ids.Set_Default).check_box.setEnabled(new_state)
        self.cellWidget(row_id, self.column_ids.Set_Forced).check_box.setEnabled(new_state)
        self.item(row_id, self.column_ids.Track_Name).setForeground(self.get_text_color(new_state))
        self.item(row_id, self.column_ids.ID).setForeground(self.get_text_color(new_state))
        self.cellWidget(row_id, self.column_ids.Track_Language).setEnabled(new_state)
        if new_state == Qt.CheckState.Checked.value or new_state == Qt.CheckState.Checked or new_state == True:
            self.item(row_id, self.column_ids.Track_Name).setFlags(
                self.item(row_id, self.column_ids.Track_Name).flags() | Qt.ItemFlag.ItemIsEditable)
        else:
            self.item(row_id, self.column_ids.Track_Name).setFlags(
                self.item(row_id, self.column_ids.Track_Name).flags() & ~Qt.ItemFlag.ItemIsEditable)

    def restore_defaults(self):
        if self.rowCount() == 0:
            return
        for row_id, track_id in enumerate(self.original_setting.keys(), start=0):
            new_row_id = self.original_setting[track_id].order
            is_enabled_state = self.original_setting[track_id].is_enabled
            is_default_state = self.original_setting[track_id].is_default
            is_forced_state = self.original_setting[track_id].is_forced
            track_name = self.original_setting[track_id].track_name
            language = self.original_setting[track_id].language
            self.set_row_value_id(track_id, new_row_id)
            self.set_row_value_is_enabled(is_enabled_state, new_row_id)
            self.set_row_value_is_default(is_default_state, new_row_id)
            self.set_row_value_is_forced(is_forced_state, new_row_id)
            self.set_row_value_track_name(track_name, new_row_id)
            self.set_row_value_language(language, row_id)
            self.update_state_of_row(row_id, is_enabled_state)
        self.update_widget()
        self.resize_track_name_column_to_fit_content()
        self.selectRow(0)
        self.update_selected_track(0, 0, 0, 0)

    def save_settings(self):
        is_there_different_track_setting = False
        is_there_deleted_tracks = False
        is_there_reorder_tracks = False
        for row_id in range(self.rowCount()):
            track_id = self.get_track_id_as_string_original_from_row(row_id=row_id)
            self.current_setting[track_id].is_enabled = int(self.cellWidget(row_id,
                                                                            self.column_ids.Enable).check_box.checkState().value)
            self.current_setting[track_id].is_default = int(self.cellWidget(row_id,
                                                                            self.column_ids.Set_Default).check_box.checkState().value)
            self.current_setting[track_id].is_forced = int(self.cellWidget(row_id,
                                                                           self.column_ids.Set_Forced).check_box.checkState().value)
            self.current_setting[track_id].track_name = self.item(row_id, self.column_ids.Track_Name).text()
            temp_language = self.cellWidget(row_id, self.column_ids.Track_Language).currentText()
            self.current_setting[track_id].language = ("[Old]" if temp_language == "" else temp_language)
            self.current_setting[track_id].order = row_id
            if not is_there_different_track_setting and self.current_setting[track_id] != self.original_setting[
                track_id]:
                is_there_different_track_setting = True
            if not self.current_setting[track_id].is_enabled:
                is_there_deleted_tracks = True
            if self.current_setting[track_id].order != self.original_setting[track_id].order:
                is_there_reorder_tracks = True

        self.is_there_different_track_setting = is_there_different_track_setting
        self.is_there_deleted_tracks = is_there_deleted_tracks
        self.is_there_reorder_tracks = is_there_reorder_tracks

    def update_selected_track(self, current_row, current_column, previous_row, previous_column):
        current_track = self.get_track_id_as_string_original_from_row(current_row)
        current_track = int(current_track)
        self.selected_track_changed.emit(current_track)

    def move_row_up(self):
        row_id = self.currentRow()
        if row_id == 0 or row_id == -1:  # -1 means no row is selected
            return
        new_row_id = row_id - 1
        self.replace_rows(new_row_id, row_id)

    def move_row_down(self):
        row_id = self.currentRow()
        if row_id + 1 == self.rowCount() or row_id == -1:  # -1 means no row is selected:
            return
        new_row_id = row_id + 1
        self.replace_rows(new_row_id, row_id)

    def replace_rows(self, new_row_id, row_id):
        self.replace_rows_value_id(new_row_id, row_id)
        self.replace_rows_value_is_enabled(new_row_id, row_id)
        self.replace_rows_value_is_default(new_row_id, row_id)
        self.replace_rows_value_is_forced(new_row_id, row_id)
        self.replace_rows_value_track_name(new_row_id, row_id)
        self.replace_rows_value_language(new_row_id, row_id)
        self.update_state_of_replaced_rows(new_row_id, row_id)
        self.selectRow(new_row_id)

    def get_track_id_as_string_original_from_row(self, row_id):
        track_id = self.item(row_id, 0).text().split(" ")[1]
        track_id_str = str(int(track_id))
        return track_id_str

    def replace_rows_value_id(self, new_row_id, row_id):
        old_track_id = self.item(row_id, 0).text().split(" ")[1]
        new_track_id = self.item(new_row_id, 0).text().split(" ")[1]
        self.set_row_value_id(track_id=new_track_id, new_row_id=row_id)
        self.set_row_value_id(track_id=old_track_id, new_row_id=new_row_id)

    def replace_rows_value_is_enabled(self, new_row_id, row_id):
        old_is_enable_check_state = self.cellWidget(row_id, self.column_ids.Enable).check_box.checkState()
        new_is_enable_check_state = self.cellWidget(new_row_id, self.column_ids.Enable).check_box.checkState()
        self.set_row_value_is_enabled(is_enabled_state=old_is_enable_check_state, new_row_id=new_row_id)
        self.set_row_value_is_enabled(is_enabled_state=new_is_enable_check_state, new_row_id=row_id)

    def replace_rows_value_is_default(self, new_row_id, row_id):
        old_is_default_check_state = self.cellWidget(row_id, self.column_ids.Set_Default).check_box.checkState()
        new_is_default_check_state = self.cellWidget(new_row_id, self.column_ids.Set_Default).check_box.checkState()
        self.set_row_value_is_default(is_default_state=old_is_default_check_state, new_row_id=new_row_id)
        self.set_row_value_is_default(is_default_state=new_is_default_check_state, new_row_id=row_id)

    def replace_rows_value_is_forced(self, new_row_id, row_id):
        old_is_forced_check_state = self.cellWidget(row_id, self.column_ids.Set_Forced).check_box.checkState()
        new_is_forced_check_state = self.cellWidget(new_row_id, self.column_ids.Set_Forced).check_box.checkState()
        self.set_row_value_is_forced(is_forced_state=old_is_forced_check_state, new_row_id=new_row_id)
        self.set_row_value_is_forced(is_forced_state=new_is_forced_check_state, new_row_id=row_id)

    def replace_rows_value_track_name(self, new_row_id, row_id):
        old_track_name = self.item(row_id, self.column_ids.Track_Name).text()
        new_track_name = self.item(new_row_id, self.column_ids.Track_Name).text()
        self.set_row_value_track_name(track_name=old_track_name, new_row_id=new_row_id)
        self.set_row_value_track_name(track_name=new_track_name, new_row_id=row_id)

    def replace_rows_value_language(self, new_row_id, row_id):
        old_track_language = self.cellWidget(row_id, self.column_ids.Track_Language).currentText()
        new_track_language = self.cellWidget(new_row_id, self.column_ids.Track_Language).currentText()
        self.set_row_value_language(language=old_track_language, new_row_id=new_row_id)
        self.set_row_value_language(language=new_track_language, new_row_id=row_id)

    def update_state_of_replaced_rows(self, new_row_id, row_id):
        old_is_enable_check_state = self.cellWidget(row_id, self.column_ids.Enable).check_box.checkState()
        new_is_enable_check_state = self.cellWidget(new_row_id, self.column_ids.Enable).check_box.checkState()
        self.update_state_of_row(row_id=row_id, new_state=old_is_enable_check_state)
        self.update_state_of_row(row_id=new_row_id, new_state=new_is_enable_check_state)

    def table_focused(self):
        if self.rowCount() > 0:
            current_row = self.currentRow()
            if current_row == -1:
                current_row = 0
            self.selectRow(current_row)
            self.update_selected_track(current_row, 0, 0, 0)
