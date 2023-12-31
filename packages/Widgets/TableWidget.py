import sys

from PySide2 import QtGui
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QPalette
from PySide2.QtWidgets import QStyledItemDelegate, QTableWidget, QStyle

from packages.Startup.Options import Options
from packages.Tabs.GlobalSetting import sort_names_like_windows


class TableWidget(QTableWidget):
    drop_folder_and_files_signal = Signal(list)

    def __init__(self):
        super().__init__()

        class StyleDelegateForQTableWidget(QStyledItemDelegate):
            color_default = QtGui.QColor("#aaedff")  # aaedff: blue Kashef

            def paint(self, painter, option, index):
                if option.state & QStyle.StateFlag.State_Selected:
                    item_color = index.data(role=Qt.ItemDataRole.DecorationRole.ForegroundRole)
                    if item_color is None:
                        item_color = Qt.GlobalColor.black
                    else:
                        item_color = item_color.color()
                    option.palette.setColor(QPalette.ColorRole.HighlightedText, item_color)
                    if Options.Dark_Mode:
                        color = self.combineColors(self.color_default, self.background(option, index), 3)
                    else:
                        color = self.combineColors(self.color_default, self.background(option, index), 2)
                    option.palette.setColor(QPalette.ColorRole.Highlight, color)
                QStyledItemDelegate.paint(self, painter, option, index)

            def background(self, option, index):
                item = self.parent().itemFromIndex(index)
                if item:
                    if item.background() != QtGui.QBrush():
                        return item.background().color()
                if self.parent().alternatingRowColors():
                    if index.row() % 2 == 1:
                        return option.palette.color(QPalette.AlternateBase)
                return option.palette.color(QPalette.Base)

            @staticmethod
            def combineColors(c1, c2, factor):
                c3 = QtGui.QColor()
                c3.setRed((c1.red() + c2.red()) // factor)
                c3.setGreen((c1.green() + c2.green()) // factor)
                c3.setBlue((c1.blue() + c2.blue()) // factor)
                return c3

        self.setItemDelegate(StyleDelegateForQTableWidget(self))

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        paths_to_add = []
        for url in urls:
            if sys.platform == "win32":
                current_path = url.path()[1:]
            else:
                current_path = url.path()
            paths_to_add.append(current_path)
        self.drop_folder_and_files_signal.emit(sort_names_like_windows(paths_to_add))
