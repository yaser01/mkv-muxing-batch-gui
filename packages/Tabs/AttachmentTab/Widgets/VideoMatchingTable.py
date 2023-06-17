from PySide2.QtGui import Qt
from PySide2.QtWidgets import QHeaderView, QTableWidgetItem, QAbstractItemView

from packages.Startup.InitializeScreenResolution import screen_size
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Widgets.TableFixedHeader import TableFixedHeaderWidget
from packages.Widgets.TableNoSelection import TableWidgetNoSelection


class VideoMatchingTable(TableFixedHeaderWidget):
    def __init__(self):
        super().__init__(primarytable=TableWidgetNoSelection(), headername="Video Name")
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.verticalScrollBar().setSingleStep(1)
        self.table.setRowCount(0)
        self.table.verticalHeader().setDefaultSectionSize(screen_size.height() // 27)

    def clear_table(self):
        self.table.setRowCount(0)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def show_files(self):
        video_file_list = GlobalSetting.VIDEO_FILES_LIST
        self.table.setRowCount(len(video_file_list))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        for i in range(len(video_file_list)):
            item = QTableWidgetItem(video_file_list[i])
            item.setToolTip(video_file_list[i])
            self.table.setItem(i, 0, item)
            item = QTableWidgetItem(str(i + 1))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setVerticalHeaderItem(i, item)
