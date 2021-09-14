import os

import PySide2
from PySide2.QtCore import Signal
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem

from packages.Startup.InitializeScreenResolution import screen_size
from packages.Widgets.TableWidget import TableWidget


class VideoTable(TableWidget):
    drop_folder_signal = Signal(str)
    drop_files_signal = Signal(list)

    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setRowCount(0)
        self.setAcceptDrops(True)
        self.disable_table_bold_column()
        self.disable_table_edit()
        self.force_select_whole_row()
        self.force_single_row_selection()
        self.make_column_expand_as_possible(column_index=0)
        self.set_row_height(new_height=screen_size.height() // 27)
        self.setup_columns()

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        files_counter = 0
        folder_counter = 0
        for url in urls:
            path_to_test = url.path()[1:]
            if os.path.isfile(path_to_test):
                files_counter += 1
            else:
                folder_counter += 1
        if urls and (folder_counter == 1 and files_counter == 0) or (folder_counter == 0 and files_counter != 0):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        files_counter = 0
        folder_counter = 0
        for url in urls:
            path_to_test = url.path()[1:]
            if os.path.isfile(path_to_test):
                files_counter += 1
            else:
                folder_counter += 1
        if urls and (folder_counter == 1 and files_counter == 0) or (folder_counter == 0 and files_counter != 0):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        path_to_test = urls[0].path()[1:]
        if not os.path.isfile(path_to_test):
            self.drop_folder_signal.emit(path_to_test)

    def disable_table_bold_column(self):
        self.horizontalHeader().setHighlightSections(False)

    def disable_table_edit(self):
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def force_select_whole_row(self):
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def make_column_expand_as_possible(self, column_index):
        header = self.horizontalHeader()
        header.setSectionResizeMode(column_index, QHeaderView.Stretch)

    def force_single_row_selection(self):
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def setup_columns(self):
        self.set_column_name(column_index=0, name="Name")
        self.set_column_name(column_index=1, name="Size")

    def set_column_name(self, column_index, name):
        column = QTableWidgetItem(name)
        column.setTextAlignment(Qt.AlignLeft)
        self.setHorizontalHeaderItem(column_index, column)

    def set_row_height(self, new_height):
        self.verticalHeader().setDefaultSectionSize(new_height)

    def resize_2nd_column(self):
        self.setColumnWidth(1, min(self.columnWidth(0) // 2, screen_size.width() // 14))

    def resizeEvent(self, event: PySide2.QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.resize_2nd_column()

    def show_files_list(self, files_names_list, files_size_list):
        self.setRowCount(len(files_names_list))
        self.set_row_height(new_height=screen_size.height() // 27)
        for i in range(len(files_names_list)):
            self.set_row_number(row_number=i + 1, row_index=i)
            self.set_row_file_name(file_name=files_names_list[i], row_index=i)
            self.set_row_file_size(file_size=files_size_list[i], row_index=i)
        self.show()

    def set_row_number(self, row_number, row_index):
        row_number_item = QTableWidgetItem(str(row_number))
        row_number_item.setTextAlignment(Qt.AlignCenter)
        self.setVerticalHeaderItem(row_index, row_number_item)

    def set_row_file_size(self, file_size, row_index):
        file_size_item = QTableWidgetItem(file_size)
        self.setItem(row_index, 1, file_size_item)

    def set_row_file_name(self, file_name, row_index):
        file_name_item = QTableWidgetItem(" " + file_name)
        self.setItem(row_index, 0, file_name_item)
