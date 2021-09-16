from PySide2.QtCore import Signal
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QHeaderView, QTableWidgetItem, QAbstractItemView

from packages.Startup.InitializeScreenResolution import screen_size
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Widgets.TableFixedHeader import TableFixedHeaderWidget
from packages.Widgets.TableWidget import TableWidget


class SubtitleMatchingTable(TableFixedHeaderWidget):
    drop_folder_and_files_signal = Signal(list)

    def __init__(self):
        super().__init__(primarytable=TableWidget(), headername="Subtitle Name")
        self.current_files_list = []
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.verticalScrollBar().setSingleStep(1)
        self.table.setRowCount(0)
        self.table.setAcceptDrops(True)
        self.table.verticalHeader().setDefaultSectionSize(screen_size.height() // 27)
        self.table.drop_folder_and_files_signal.connect(self.drop_files)

    def drop_files(self, paths_list):
        self.drop_folder_and_files_signal.emit(paths_list)

    def clear_table(self):
        self.table.setRowCount(0)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def show_files(self):
        files_list = GlobalSetting.SUBTITLE_FILES_LIST
        self.table.setRowCount(len(files_list))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        for i in range(len(files_list)):
            item = QTableWidgetItem(" " + files_list[i])
            self.table.setItem(i, 0, item)
            item = QTableWidgetItem(str(i + 1))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setVerticalHeaderItem(i, item)
        self.current_files_list = files_list[:]  # for copy the rel elements not refrences

    def show_files_after_swapping(self):
        files_list = GlobalSetting.SUBTITLE_FILES_LIST
        for i in range(len(files_list)):
            if files_list[i] != self.current_files_list[i]:
                item = QTableWidgetItem(" " + files_list[i])
                self.table.setItem(i, 0, item)
                item = QTableWidgetItem(str(i + 1))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setVerticalHeaderItem(i, item)
                self.current_files_list[i] = files_list[i]

    def clear_selection(self):
        self.table.clearSelection()

    def select_row(self, row_id):
        self.table.selectRow(row_id)
        self.table.setFocus()
