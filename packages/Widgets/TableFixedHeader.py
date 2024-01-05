import PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QPaintEvent
from PySide6.QtWidgets import QGridLayout, QTableWidgetItem, \
    QHeaderView, QAbstractItemView, QTableWidget

from packages.Widgets.TableNoSelection import TableWidgetNoSelection


class TableFixedHeaderWidget(QTableWidget):
    def __init__(self, primarytable=QTableWidget(), headername="Test", numberofcolumn=1):
        QTableWidget.__init__(self)
        self.table = primarytable
        self.table.setColumnCount(numberofcolumn)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.column0 = QTableWidgetItem(headername)
        self.column0.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setHorizontalHeaderItem(0, self.column0)

        self.tableHeader = TableWidgetNoSelection()
        self.column1 = QTableWidgetItem(headername)
        self.column1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tableHeader.setColumnCount(numberofcolumn)
        self.tableHeader.setHorizontalHeaderItem(0, self.column1)
        self.tableHeader.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableHeader.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.tableHeader.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tableHeader.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tableHeader.horizontalHeader().setHighlightSections(False)

        self.tableLayout = QGridLayout(self)
        self.tableLayout.addWidget(self.table, 0, 0, -1, 1)
        self.tableLayout.addWidget(self.tableHeader, 0, 0, -1, 1)
        self.tableLayout.setContentsMargins(0, 0, 0, 0)
        self.tableLayout.setSpacing(0)

    def takeupdate(self):
        # make sure that new header place exactly on old header [Width Checker]
        if self.table.verticalScrollBar().isVisible() and self.table.isEnabled():
            new_width = self.table.width() - self.table.verticalScrollBar().width()
            self.tableHeader.resize(new_width, self.tableHeader.height())
        else:
            new_width = self.table.width()
            self.tableHeader.resize(new_width, self.tableHeader.height())

        # make sure that new header place exactly on old header [Height Checker]
        self.tableHeader.setMinimumHeight(self.table.horizontalHeader().height())
        self.tableHeader.setMaximumHeight(self.table.horizontalHeader().height())

        # make sure that new header place exactly on old header [Position Checker]
        self.tableHeader.move(self.table.pos())

    def update_row_size(self):
        new_column_width = self.tableHeader.width()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        for i in range(self.table.rowCount()):
            column_font = self.table.item(i, 0).font()
            column_font_metrics = QFontMetrics(column_font)
            new_column_width = max(new_column_width, column_font_metrics.horizontalAdvance(
                self.table.item(i, 0).text()))
        new_column_width += 15
        self.table.setColumnWidth(0, new_column_width)

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.update_row_size()
        self.takeupdate()
        super().paintEvent(a0)
        self.update_row_size()
        self.takeupdate()

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent):
        self.takeupdate()
        super().resizeEvent(event)
        self.takeupdate()
